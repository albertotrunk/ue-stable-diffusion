# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
MLflow Logger
-------------
"""
import logging
import os
import re
from argparse import Namespace
from time import time
from typing import Any, Dict, Mapping, Optional, Union

from pytorch_lightning.loggers.logger import Logger, rank_zero_experiment
from pytorch_lightning.utilities.imports import _module_available
from pytorch_lightning.utilities.logger import _add_prefix, _convert_params, _flatten_dict
from pytorch_lightning.utilities.rank_zero import rank_zero_only, rank_zero_warn

log = logging.getLogger(__name__)
LOCAL_FILE_URI_PREFIX = "file:"
_MLFLOW_AVAILABLE = _module_available("mlflow")
try:
    import mlflow
    from mlflow.tracking import context, MlflowClient
    from mlflow.utils.mlflow_tags import MLFLOW_RUN_NAME
# todo: there seems to be still some remaining import error with Conda env
except ModuleNotFoundError:
    _MLFLOW_AVAILABLE = False
    mlflow, MlflowClient, context = None, None, None
    MLFLOW_RUN_NAME = "mlflow.runName"

# before v1.1.0
if hasattr(context, "resolve_tags"):
    from mlflow.tracking.context import resolve_tags


# since v1.1.0
elif hasattr(context, "registry"):
    from mlflow.tracking.context.registry import resolve_tags
else:

    def resolve_tags(tags: Optional[Dict] = None) -> Optional[Dict]:
        """
        Args:
            tags: A dictionary of tags to override. If specified, tags passed in this argument will
                 override those inferred from the context.

        Returns: A dictionary of resolved tags.

        Note:
            See ``mlflow.tracking.context.registry`` for more details.
        """
        return tags


class MLFlowLogger(Logger):
    """Log using `MLflow <https://mlflow.org>`_.

    Install it with pip:

    .. code-block:: bash

        pip install mlflow

    .. code-block:: python

        from pytorch_lightning import Trainer
        from pytorch_lightning.loggers import MLFlowLogger

        mlf_logger = MLFlowLogger(experiment_name="lightning_logs", tracking_uri="file:./ml-runs")
        trainer = Trainer(logger=mlf_logger)

    Use the logger anywhere in your :class:`~pytorch_lightning.core.module.LightningModule` as follows:

    .. code-block:: python

        from pytorch_lightning import LightningModule


        class LitModel(LightningModule):
            def training_step(self, batch, batch_idx):
                # example
                self.logger.experiment.whatever_ml_flow_supports(...)

            def any_lightning_module_function_or_hook(self):
                self.logger.experiment.whatever_ml_flow_supports(...)

    Args:
        experiment_name: The name of the experiment.
        run_name: Name of the new run. The `run_name` is internally stored as a ``mlflow.runName`` tag.
            If the ``mlflow.runName`` tag has already been set in `tags`, the value is overridden by the `run_name`.
        tracking_uri: Address of local or remote tracking server.
            If not provided, defaults to `MLFLOW_TRACKING_URI` environment variable if set, otherwise it falls
            back to `file:<save_dir>`.
        tags: A dictionary tags for the experiment.
        save_dir: A path to a local directory where the MLflow runs get saved.
            Defaults to `./mlflow` if `tracking_uri` is not provided.
            Has no effect if `tracking_uri` is provided.
        prefix: A string to put at the beginning of metric keys.
        artifact_location: The location to store run artifacts. If not provided, the server picks an appropriate
            default.
        run_id: The run identifier of the experiment. If not provided, a new run is started.

    Raises:
        ModuleNotFoundError:
            If required MLFlow package is not installed on the device.
    """

    LOGGER_JOIN_CHAR = "-"

    def __init__(
        self,
        experiment_name: str = "lightning_logs",
        run_name: Optional[str] = None,
        tracking_uri: Optional[str] = os.getenv("MLFLOW_TRACKING_URI"),
        tags: Optional[Dict[str, Any]] = None,
        save_dir: Optional[str] = "./mlruns",
        prefix: str = "",
        artifact_location: Optional[str] = None,
        run_id: Optional[str] = None,
    ):
        if mlflow is None:
            raise ModuleNotFoundError(
                "You want to use `mlflow` logger which is not installed yet, install it with `pip install mlflow`."
            )
        super().__init__()
        if not tracking_uri:
            tracking_uri = f"{LOCAL_FILE_URI_PREFIX}{save_dir}"

        self._experiment_name = experiment_name
        self._experiment_id: Optional[str] = None
        self._tracking_uri = tracking_uri
        self._run_name = run_name
        self._run_id = run_id
        self.tags = tags
        self._prefix = prefix
        self._artifact_location = artifact_location

        self._initialized = False

        self._mlflow_client = MlflowClient(tracking_uri)

    @property  # type: ignore[misc]
    @rank_zero_experiment
    def experiment(self) -> MlflowClient:
        r"""
        Actual MLflow object. To use MLflow features in your
        :class:`~pytorch_lightning.core.module.LightningModule` do the following.

        Example::

            self.logger.experiment.some_mlflow_function()

        """

        if self._initialized:
            return self._mlflow_client

        if self._run_id is not None:
            run = self._mlflow_client.get_run(self._run_id)
            self._experiment_id = run.info.experiment_id
            self._initialized = True
            return self._mlflow_client

        if self._experiment_id is None:
            expt = self._mlflow_client.get_experiment_by_name(self._experiment_name)
            if expt is not None:
                self._experiment_id = expt.experiment_id
            else:
                log.warning(f"Experiment with name {self._experiment_name} not found. Creating it.")
                self._experiment_id = self._mlflow_client.create_experiment(
                    name=self._experiment_name, artifact_location=self._artifact_location
                )

        if self._run_id is None:
            if self._run_name is not None:
                self.tags = self.tags or {}
                if MLFLOW_RUN_NAME in self.tags:
                    log.warning(
                        f"The tag {MLFLOW_RUN_NAME} is found in tags. The value will be overridden by {self._run_name}."
                    )
                self.tags[MLFLOW_RUN_NAME] = self._run_name
            run = self._mlflow_client.create_run(experiment_id=self._experiment_id, tags=resolve_tags(self.tags))
            self._run_id = run.info.run_id
        self._initialized = True
        return self._mlflow_client

    @property
    def run_id(self) -> Optional[str]:
        """Create the experiment if it does not exist to get the run id.

        Returns:
            The run id.
        """
        _ = self.experiment
        return self._run_id

    @property
    def experiment_id(self) -> Optional[str]:
        """Create the experiment if it does not exist to get the experiment id.

        Returns:
            The experiment id.
        """
        _ = self.experiment
        return self._experiment_id

    @rank_zero_only
    def log_hyperparams(self, params: Union[Dict[str, Any], Namespace]) -> None:
        params = _convert_params(params)
        params = _flatten_dict(params)
        for k, v in params.items():
            if len(str(v)) > 250:
                rank_zero_warn(
                    f"Mlflow only allows parameters with up to 250 characters. Discard {k}={v}", category=RuntimeWarning
                )
                continue

            self.experiment.log_param(self.run_id, k, v)

    @rank_zero_only
    def log_metrics(self, metrics: Mapping[str, float], step: Optional[int] = None) -> None:
        assert rank_zero_only.rank == 0, "experiment tried to log from global_rank != 0"

        metrics = _add_prefix(metrics, self._prefix, self.LOGGER_JOIN_CHAR)

        timestamp_ms = int(time() * 1000)
        for k, v in metrics.items():
            if isinstance(v, str):
                log.warning(f"Discarding metric with string value {k}={v}.")
                continue

            new_k = re.sub("[^a-zA-Z0-9_/. -]+", "", k)
            if k != new_k:
                rank_zero_warn(
                    "MLFlow only allows '_', '/', '.' and ' ' special characters in metric name."
                    f" Replacing {k} with {new_k}.",
                    category=RuntimeWarning,
                )
                k = new_k

            self.experiment.log_metric(self.run_id, k, v, timestamp_ms, step)

    @rank_zero_only
    def finalize(self, status: str = "FINISHED") -> None:
        super().finalize(status)
        status = "FINISHED" if status == "success" else status
        if self.experiment.get_run(self.run_id):
            self.experiment.set_terminated(self.run_id, status)

    @property
    def save_dir(self) -> Optional[str]:
        """The root file directory in which MLflow experiments are saved.

        Return:
            Local path to the root experiment directory if the tracking uri is local.
            Otherwise returns `None`.
        """
        if self._tracking_uri.startswith(LOCAL_FILE_URI_PREFIX):
            return self._tracking_uri.lstrip(LOCAL_FILE_URI_PREFIX)

    @property
    def name(self) -> Optional[str]:
        """Get the experiment id.

        Returns:
            The experiment id.
        """
        return self.experiment_id

    @property
    def version(self) -> Optional[str]:
        """Get the run id.

        Returns:
            The run id.
        """
        return self.run_id
