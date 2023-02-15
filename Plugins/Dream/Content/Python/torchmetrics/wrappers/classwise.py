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
from typing import Any, Callable, Dict, List, Optional

from torch import Tensor

from torchmetrics import Metric


class ClasswiseWrapper(Metric):
    """Wrapper class for altering the output of classification metrics that returns multiple values to include
    label information.

    Args:
        metric: base metric that should be wrapped. It is assumed that the metric outputs a single
            tensor that is split along the first dimension.
        labels: list of strings indicating the different classes.

    Example:
        >>> import torch
        >>> _ = torch.manual_seed(42)
        >>> from torchmetrics import ClasswiseWrapper
        >>> from torchmetrics.classification import MulticlassAccuracy
        >>> metric = ClasswiseWrapper(MulticlassAccuracy(num_classes=3, average=None))
        >>> preds = torch.randn(10, 3).softmax(dim=-1)
        >>> target = torch.randint(3, (10,))
        >>> metric(preds, target)  # doctest: +NORMALIZE_WHITESPACE
        {'multiclassaccuracy_0': tensor(0.5000),
        'multiclassaccuracy_1': tensor(0.7500),
        'multiclassaccuracy_2': tensor(0.)}

    Example (labels as list of strings):
        >>> import torch
        >>> from torchmetrics import ClasswiseWrapper
        >>> from torchmetrics.classification import MulticlassAccuracy
        >>> metric = ClasswiseWrapper(
        ...    MulticlassAccuracy(num_classes=3, average=None),
        ...    labels=["horse", "fish", "dog"]
        ... )
        >>> preds = torch.randn(10, 3).softmax(dim=-1)
        >>> target = torch.randint(3, (10,))
        >>> metric(preds, target)  # doctest: +NORMALIZE_WHITESPACE
        {'multiclassaccuracy_horse': tensor(0.3333),
        'multiclassaccuracy_fish': tensor(0.6667),
        'multiclassaccuracy_dog': tensor(0.)}

    Example (in metric collection):
        >>> import torch
        >>> from torchmetrics import ClasswiseWrapper, MetricCollection
        >>> from torchmetrics.classification import MulticlassAccuracy, MulticlassRecall
        >>> labels = ["horse", "fish", "dog"]
        >>> metric = MetricCollection(
        ...     {'multiclassaccuracy': ClasswiseWrapper(MulticlassAccuracy(num_classes=3, average=None), labels),
        ...     'multiclassrecall': ClasswiseWrapper(MulticlassRecall(num_classes=3, average=None), labels)}
        ... )
        >>> preds = torch.randn(10, 3).softmax(dim=-1)
        >>> target = torch.randint(3, (10,))
        >>> metric(preds, target)  # doctest: +NORMALIZE_WHITESPACE
        {'multiclassaccuracy_horse': tensor(0.),
         'multiclassaccuracy_fish': tensor(0.3333),
         'multiclassaccuracy_dog': tensor(0.4000),
         'multiclassrecall_horse': tensor(0.),
         'multiclassrecall_fish': tensor(0.3333),
         'multiclassrecall_dog': tensor(0.4000)}
    """

    def __init__(self, metric: Metric, labels: Optional[List[str]] = None) -> None:
        super().__init__()
        if not isinstance(metric, Metric):
            raise ValueError(f"Expected argument `metric` to be an instance of `torchmetrics.Metric` but got {metric}")
        if labels is not None and not (isinstance(labels, list) and all(isinstance(lab, str) for lab in labels)):
            raise ValueError(f"Expected argument `labels` to either be `None` or a list of strings but got {labels}")
        self.metric = metric
        self.labels = labels
        self._update_count = 1

    def _convert(self, x: Tensor) -> Dict[str, Any]:
        name = self.metric.__class__.__name__.lower()
        if self.labels is None:
            return {f"{name}_{i}": val for i, val in enumerate(x)}
        return {f"{name}_{lab}": val for lab, val in zip(self.labels, x)}

    def forward(self, *args: Any, **kwargs: Any) -> Any:
        return self._convert(self.metric(*args, **kwargs))

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.metric.update(*args, **kwargs)

    def compute(self) -> Dict[str, Tensor]:
        return self._convert(self.metric.compute())

    def reset(self) -> None:
        self.metric.reset()

    def _wrap_update(self, update: Callable) -> Callable:
        """Overwrite to do nothing."""
        return update

    def _wrap_compute(self, compute: Callable) -> Callable:
        """Overwrite to do nothing."""
        return compute
