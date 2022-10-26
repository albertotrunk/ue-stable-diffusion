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
from typing import Optional

import torch
from torch import Tensor, tensor

from torchmetrics.utilities.checks import _check_retrieval_functional_inputs


def retrieval_hit_rate(preds: Tensor, target: Tensor, k: Optional[int] = None) -> Tensor:
    """Computes the hit rate (for information retrieval). The hit rate is 1.0 if there is at least one relevant
    document among all the top `k` retrieved documents.

    ``preds`` and ``target`` should be of the same shape and live on the same device. If no ``target`` is ``True``,
    ``0`` is returned. ``target`` must be either `bool` or `integers` and ``preds`` must be ``float``,
    otherwise an error is raised. If you want to measure HitRate@K, ``k`` must be a positive integer.

    Args:
        preds: estimated probabilities of each document to be relevant.
        target: ground truth about each document being relevant or not.
        k: consider only the top k elements (default: `None`, which considers them all)

    Returns:
        a single-value tensor with the hit rate (at ``k``) of the predictions ``preds`` w.r.t. the labels ``target``.

    Raises:
        ValueError:
            If ``k`` parameter is not `None` or an integer larger than 0

    Example:
        >>> preds = tensor([0.2, 0.3, 0.5])
        >>> target = tensor([True, False, True])
        >>> retrieval_hit_rate(preds, target, k=2)
        tensor(1.)
    """
    preds, target = _check_retrieval_functional_inputs(preds, target)

    if k is None:
        k = preds.shape[-1]

    if not (isinstance(k, int) and k > 0):
        raise ValueError("`k` has to be a positive integer or None")

    relevant = target[torch.argsort(preds, dim=-1, descending=True)][:k].sum()
    return (relevant > 0).float()
