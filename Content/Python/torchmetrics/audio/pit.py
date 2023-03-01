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
from typing import Any, Callable, Dict

from torch import Tensor, tensor
from typing_extensions import Literal

from torchmetrics.functional.audio.pit import permutation_invariant_training
from torchmetrics.metric import Metric


class PermutationInvariantTraining(Metric):
    """Calculates `Permutation invariant training`_ (PIT) that can evaluate models for speaker independent multi-
    talker speech separation in a permutation invariant way.

    As input to ``forward`` and ``update`` the metric accepts the following input

    - ``preds`` (:class:`~torch.Tensor`): float tensor with shape ``(batch_size,num_speakers,...)``
    - ``target`` (:class:`~torch.Tensor`): float tensor with shape ``(batch_size,num_speakers,...)``

    As output of `forward` and `compute` the metric returns the following output

    - ``pesq`` (:class:`~torch.Tensor`): float scalar tensor with average PESQ value over samples

    Args:
        metric_func:
            a metric function accept a batch of target and estimate,
            i.e. ``metric_func(preds[:, i, ...], target[:, j, ...])``, and returns a batch of metric
            tensors ``(batch,)``
        eval_func:
            the function to find the best permutation, can be 'min' or 'max', i.e. the smaller the better
            or the larger the better.
        kwargs: Additional keyword arguments for either the ``metric_func`` or distributed communication,
            see :ref:`Metric kwargs` for more info.

    Example:
        >>> import torch
        >>> from torchmetrics import PermutationInvariantTraining
        >>> from torchmetrics.functional import scale_invariant_signal_noise_ratio
        >>> _ = torch.manual_seed(42)
        >>> preds = torch.randn(3, 2, 5) # [batch, spk, time]
        >>> target = torch.randn(3, 2, 5) # [batch, spk, time]
        >>> pit = PermutationInvariantTraining(scale_invariant_signal_noise_ratio, 'max')
        >>> pit(preds, target)
        tensor(-2.1065)
    """

    full_state_update: bool = False
    is_differentiable: bool = True
    sum_pit_metric: Tensor
    total: Tensor

    def __init__(
        self,
        metric_func: Callable,
        eval_func: Literal["max", "min"] = "max",
        **kwargs: Any,
    ) -> None:
        base_kwargs: Dict[str, Any] = {
            "dist_sync_on_step": kwargs.pop("dist_sync_on_step", False),
            "process_group": kwargs.pop("process_group", None),
            "dist_sync_fn": kwargs.pop("dist_sync_fn", None),
        }
        super().__init__(**base_kwargs)
        self.metric_func = metric_func
        self.eval_func = eval_func
        self.kwargs = kwargs

        self.add_state("sum_pit_metric", default=tensor(0.0), dist_reduce_fx="sum")
        self.add_state("total", default=tensor(0), dist_reduce_fx="sum")

    def update(self, preds: Tensor, target: Tensor) -> None:
        """Update state with predictions and targets."""
        pit_metric = permutation_invariant_training(preds, target, self.metric_func, self.eval_func, **self.kwargs)[0]

        self.sum_pit_metric += pit_metric.sum()
        self.total += pit_metric.numel()

    def compute(self) -> Tensor:
        """Computes metric."""
        return self.sum_pit_metric / self.total
