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

from typing import Any, List, Union

from torch import Tensor, tensor

from torchmetrics.functional.text.wip import _wip_compute, _wip_update
from torchmetrics.metric import Metric


class WordInfoPreserved(Metric):
    r"""Word Information Preserved (`WIP`_) is a metric of the performance of an automatic speech recognition
    system. This value indicates the percentage of words that were correctly predicted between a set of ground-
    truth sentences and a set of hypothesis sentences. The higher the value, the better the performance of the ASR
    system with a WordInfoPreserved of 1 being a perfect score. Word Information Preserved rate can then be
    computed as:

    .. math::
        wip = \frac{C}{N} + \frac{C}{P}

    where:

        - :math:`C` is the number of correct words,
        - :math:`N` is the number of words in the reference
        - :math:`P` is the number of words in the prediction

    As input to ``forward`` and ``update`` the metric accepts the following input:

    - ``preds`` (:class:`~List`): Transcription(s) to score as a string or list of strings
    - ``target`` (:class:`~List`): Reference(s) for each speech input as a string or list of strings

    As output of ``forward`` and ``compute`` the metric returns the following output:

    - ``wip`` (:class:`~torch.Tensor`): A tensor with the Word Information Preserved score

    Args:
        kwargs: Additional keyword arguments, see :ref:`Metric kwargs` for more info.

    Examples:
        >>> from torchmetrics import WordInfoPreserved
        >>> preds = ["this is the prediction", "there is an other sample"]
        >>> target = ["this is the reference", "there is another one"]
        >>> wip = WordInfoPreserved()
        >>> wip(preds, target)
        tensor(0.3472)
    """
    is_differentiable: bool = False
    higher_is_better: bool = False
    full_state_update: bool = False

    errors: Tensor
    preds_total: Tensor
    target_total: Tensor

    def __init__(
        self,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.add_state("errors", tensor(0.0), dist_reduce_fx="sum")
        self.add_state("target_total", tensor(0.0), dist_reduce_fx="sum")
        self.add_state("preds_total", tensor(0.0), dist_reduce_fx="sum")

    def update(self, preds: Union[str, List[str]], target: Union[str, List[str]]) -> None:
        """Update state with predictions and targets."""
        errors, target_total, preds_total = _wip_update(preds, target)
        self.errors += errors
        self.target_total += target_total
        self.preds_total += preds_total

    def compute(self) -> Tensor:
        """Calculate the Word Information Preserved."""
        return _wip_compute(self.errors, self.target_total, self.preds_total)
