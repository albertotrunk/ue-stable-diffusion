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
import logging
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
import torch
from torch import IntTensor, Tensor

from torchmetrics.metric import Metric
from torchmetrics.utilities.imports import _PYCOCOTOOLS_AVAILABLE, _TORCHVISION_GREATER_EQUAL_0_8

if _TORCHVISION_GREATER_EQUAL_0_8:
    from torchvision.ops import box_area, box_convert, box_iou
else:
    box_convert = box_iou = box_area = None
    __doctest_skip__ = ["MeanAveragePrecision"]

if _PYCOCOTOOLS_AVAILABLE:
    import pycocotools.mask as mask_utils
else:
    mask_utils = None
    __doctest_skip__ = ["MeanAveragePrecision"]


log = logging.getLogger(__name__)


def compute_area(input: List[Any], iou_type: str = "bbox") -> Tensor:
    """Compute area of input depending on the specified iou_type.

    Default output for empty input is :class:`~torch.Tensor`
    """
    if len(input) == 0:

        return Tensor([])

    if iou_type == "bbox":
        return box_area(torch.stack(input))
    elif iou_type == "segm":

        input = [{"size": i[0], "counts": i[1]} for i in input]
        area = torch.tensor(mask_utils.area(input).astype("float"))

        return area
    else:
        raise Exception(f"IOU type {iou_type} is not supported")


def compute_iou(
    det: List[Any],
    gt: List[Any],
    iou_type: str = "bbox",
) -> Tensor:
    """Compute IOU between detections and ground-truth using the specified iou_type."""

    if iou_type == "bbox":
        return box_iou(torch.stack(det), torch.stack(gt))
    elif iou_type == "segm":
        return _segm_iou(det, gt)
    else:
        raise Exception(f"IOU type {iou_type} is not supported")


class BaseMetricResults(dict):
    """Base metric class, that allows fields for pre-defined metrics."""

    def __getattr__(self, key: str) -> Tensor:
        # Using this you get the correct error message, an AttributeError instead of a KeyError
        if key in self:
            return self[key]
        raise AttributeError(f"No such attribute: {key}")

    def __setattr__(self, key: str, value: Tensor) -> None:
        self[key] = value

    def __delattr__(self, key: str) -> None:
        if key in self:
            del self[key]
        raise AttributeError(f"No such attribute: {key}")


class MAPMetricResults(BaseMetricResults):
    """Class to wrap the final mAP results."""

    __slots__ = ("map", "map_50", "map_75", "map_small", "map_medium", "map_large")


class MARMetricResults(BaseMetricResults):
    """Class to wrap the final mAR results."""

    __slots__ = ("mar_1", "mar_10", "mar_100", "mar_small", "mar_medium", "mar_large")


class COCOMetricResults(BaseMetricResults):
    """Class to wrap the final COCO metric results including various mAP/mAR values."""

    __slots__ = (
        "map",
        "map_50",
        "map_75",
        "map_small",
        "map_medium",
        "map_large",
        "mar_1",
        "mar_10",
        "mar_100",
        "mar_small",
        "mar_medium",
        "mar_large",
        "map_per_class",
        "mar_100_per_class",
    )


def _segm_iou(det: List[Tuple[np.ndarray, np.ndarray]], gt: List[Tuple[np.ndarray, np.ndarray]]) -> Tensor:
    """
    Compute IOU between detections and ground-truths using mask-IOU. Based on pycocotools toolkit for mask_utils
    Args:
       det: A list of detection masks as ``[(RLE_SIZE, RLE_COUNTS)]``, where ``RLE_SIZE`` is (width, height) dimension
           of the input and RLE_COUNTS is its RLE representation;

       gt: A list of ground-truth masks as ``[(RLE_SIZE, RLE_COUNTS)]``, where ``RLE_SIZE`` is (width, height) dimension
           of the input and RLE_COUNTS is its RLE representation;

    """

    det_coco_format = [{"size": i[0], "counts": i[1]} for i in det]
    gt_coco_format = [{"size": i[0], "counts": i[1]} for i in gt]

    return torch.tensor(mask_utils.iou(det_coco_format, gt_coco_format, [False for _ in gt]))


def _input_validator(
    preds: Sequence[Dict[str, Tensor]], targets: Sequence[Dict[str, Tensor]], iou_type: str = "bbox"
) -> None:
    """Ensure the correct input format of `preds` and `targets`"""
    if not isinstance(preds, Sequence):
        raise ValueError("Expected argument `preds` to be of type Sequence")
    if not isinstance(targets, Sequence):
        raise ValueError("Expected argument `target` to be of type Sequence")
    if len(preds) != len(targets):
        raise ValueError("Expected argument `preds` and `target` to have the same length")
    iou_attribute = "boxes" if iou_type == "bbox" else "masks"

    for k in [iou_attribute, "scores", "labels"]:
        if any(k not in p for p in preds):
            raise ValueError(f"Expected all dicts in `preds` to contain the `{k}` key")

    for k in [iou_attribute, "labels"]:
        if any(k not in p for p in targets):
            raise ValueError(f"Expected all dicts in `target` to contain the `{k}` key")

    if any(type(pred[iou_attribute]) is not Tensor for pred in preds):
        raise ValueError(f"Expected all {iou_attribute} in `preds` to be of type Tensor")
    if any(type(pred["scores"]) is not Tensor for pred in preds):
        raise ValueError("Expected all scores in `preds` to be of type Tensor")
    if any(type(pred["labels"]) is not Tensor for pred in preds):
        raise ValueError("Expected all labels in `preds` to be of type Tensor")
    if any(type(target[iou_attribute]) is not Tensor for target in targets):
        raise ValueError(f"Expected all {iou_attribute} in `target` to be of type Tensor")
    if any(type(target["labels"]) is not Tensor for target in targets):
        raise ValueError("Expected all labels in `target` to be of type Tensor")

    for i, item in enumerate(targets):
        if item[iou_attribute].size(0) != item["labels"].size(0):
            raise ValueError(
                f"Input {iou_attribute} and labels of sample {i} in targets have a"
                f" different length (expected {item[iou_attribute].size(0)} labels, got {item['labels'].size(0)})"
            )
    for i, item in enumerate(preds):
        if not (item[iou_attribute].size(0) == item["labels"].size(0) == item["scores"].size(0)):
            raise ValueError(
                f"Input {iou_attribute}, labels and scores of sample {i} in predictions have a"
                f" different length (expected {item[iou_attribute].size(0)} labels and scores,"
                f" got {item['labels'].size(0)} labels and {item['scores'].size(0)})"
            )


def _fix_empty_tensors(boxes: Tensor) -> Tensor:
    """Empty tensors can cause problems in DDP mode, this methods corrects them."""

    if boxes.numel() == 0 and boxes.ndim == 1:
        return boxes.unsqueeze(0)
    return boxes


class MeanAveragePrecision(Metric):
    r"""Computes the `Mean-Average-Precision (mAP) and Mean-Average-Recall (mAR)`_ for object detection predictions.
    Optionally, the mAP and mAR values can be calculated per class.

    Predicted boxes and targets have to be in Pascal VOC format
    (xmin-top left, ymin-top left, xmax-bottom right, ymax-bottom right).
    See the :meth:`update` method for more information about the input format to this metric.

    As input to ``forward`` and ``update`` the metric accepts the following input:

    - ``preds`` (:class:`~List`): A list consisting of dictionaries each containing the key-values
      (each dictionary corresponds to a single image). Parameters that should be provided per dict

        - boxes: (:class:`~torch.FloatTensor`) of shape ``(num_boxes, 4)`` containing ``num_boxes`` detection
          boxes of the format specified in the constructor.
          By default, this method expects ``(xmin, ymin, xmax, ymax)`` in absolute image coordinates.
        - scores: :class:`~torch.FloatTensor` of shape ``(num_boxes)`` containing detection scores for the boxes.
        - labels: :class:`~torch.IntTensor` of shape ``(num_boxes)`` containing 0-indexed detection classes for
          the boxes.
        - masks: :class:`~torch.bool` of shape ``(num_boxes, image_height, image_width)`` containing boolean masks.
          Only required when `iou_type="segm"`.

    - ``target`` (:class:`~List`) A list consisting of dictionaries each containing the key-values
      (each dictionary corresponds to a single image). Parameters that should be provided per dict:

        - boxes: :class:`~torch.FloatTensor` of shape ``(num_boxes, 4)`` containing ``num_boxes`` ground truth
          boxes of the format specified in the constructor.
          By default, this method expects ``(xmin, ymin, xmax, ymax)`` in absolute image coordinates.
        - labels: :class:`~torch.IntTensor` of shape ``(num_boxes)`` containing 0-indexed ground truth
          classes for the boxes.
        - masks: :class:`~torch.bool` of shape ``(num_boxes, image_height, image_width)`` containing boolean masks.
          Only required when `iou_type="segm"`.

    As output of ``forward`` and ``compute`` the metric returns the following output:

    - ``map_dict``: A dictionary containing the following key-values:

        - map: (:class:`~torch.Tensor`)
        - map_small: (:class:`~torch.Tensor`)
        - map_medium:(:class:`~torch.Tensor`)
        - map_large: (:class:`~torch.Tensor`)
        - mar_1: (:class:`~torch.Tensor`)
        - mar_10: (:class:`~torch.Tensor`)
        - mar_100: (:class:`~torch.Tensor`)
        - mar_small: (:class:`~torch.Tensor`)
        - mar_medium: (:class:`~torch.Tensor`)
        - mar_large: (:class:`~torch.Tensor`)
        - map_50: (:class:`~torch.Tensor`) (-1 if 0.5 not in the list of iou thresholds)
        - map_75: (:class:`~torch.Tensor`) (-1 if 0.75 not in the list of iou thresholds)
        - map_per_class: (:class:`~torch.Tensor`) (-1 if class metrics are disabled)
        - mar_100_per_class: (:class:`~torch.Tensor`) (-1 if class metrics are disabled)

    For an example on how to use this metric check the `torchmetrics mAP example`_.

    .. note::
        ``map`` score is calculated with @[ IoU=self.iou_thresholds | area=all | max_dets=max_detection_thresholds ].
        Caution: If the initialization parameters are changed, dictionary keys for mAR can change as well.
        The default properties are also accessible via fields and will raise an ``AttributeError`` if not available.

    .. note::
        This metric is following the mAP implementation of
        `pycocotools <https://github.com/cocodataset/cocoapi/tree/master/PythonAPI/pycocotools>`_,
        a standard implementation for the mAP metric for object detection.

    .. note::
        This metric requires you to have `torchvision` version 0.8.0 or newer installed
        (with corresponding version 1.7.0 of torch or newer). This metric requires `pycocotools`
        installed when iou_type is `segm`. Please install with ``pip install torchvision`` or
        ``pip install torchmetrics[detection]``.

    Args:
        box_format:
            Input format of given boxes. Supported formats are ``[`xyxy`, `xywh`, `cxcywh`]``.
        iou_type:
            Type of input (either masks or bounding-boxes) used for computing IOU.
            Supported IOU types are ``["bbox", "segm"]``.
            If using ``"segm"``, masks should be provided (see :meth:`update`).
        iou_thresholds:
            IoU thresholds for evaluation. If set to ``None`` it corresponds to the stepped range ``[0.5,...,0.95]``
            with step ``0.05``. Else provide a list of floats.
        rec_thresholds:
            Recall thresholds for evaluation. If set to ``None`` it corresponds to the stepped range ``[0,...,1]``
            with step ``0.01``. Else provide a list of floats.
        max_detection_thresholds:
            Thresholds on max detections per image. If set to `None` will use thresholds ``[1, 10, 100]``.
            Else, please provide a list of ints.
        class_metrics:
            Option to enable per-class metrics for mAP and mAR_100. Has a performance impact.
        kwargs: Additional keyword arguments, see :ref:`Metric kwargs` for more info.

    Raises:
        ModuleNotFoundError:
            If ``torchvision`` is not installed or version installed is lower than 0.8.0
        ModuleNotFoundError:
            If ``iou_type`` is equal to ``seqm`` and ``pycocotools`` is not installed
        ValueError:
            If ``class_metrics`` is not a boolean
        ValueError:
            If ``preds`` is not of type (:class:`~List[Dict[str, Tensor]]`)
        ValueError:
            If ``target`` is not of type ``List[Dict[str, Tensor]]``
        ValueError:
            If ``preds`` and ``target`` are not of the same length
        ValueError:
            If any of ``preds.boxes``, ``preds.scores`` and ``preds.labels`` are not of the same length
        ValueError:
            If any of ``target.boxes`` and ``target.labels`` are not of the same length
        ValueError:
            If any box is not type float and of length 4
        ValueError:
            If any class is not type int and of length 1
        ValueError:
            If any score is not type float and of length 1

    Example:
        >>> import torch
        >>> from torchmetrics.detection.mean_ap import MeanAveragePrecision
        >>> preds = [
        ...   dict(
        ...     boxes=torch.tensor([[258.0, 41.0, 606.0, 285.0]]),
        ...     scores=torch.tensor([0.536]),
        ...     labels=torch.tensor([0]),
        ...   )
        ... ]
        >>> target = [
        ...   dict(
        ...     boxes=torch.tensor([[214.0, 41.0, 562.0, 285.0]]),
        ...     labels=torch.tensor([0]),
        ...   )
        ... ]
        >>> metric = MeanAveragePrecision()
        >>> metric.update(preds, target)
        >>> from pprint import pprint
        >>> pprint(metric.compute())
        {'map': tensor(0.6000),
         'map_50': tensor(1.),
         'map_75': tensor(1.),
         'map_large': tensor(0.6000),
         'map_medium': tensor(-1.),
         'map_per_class': tensor(-1.),
         'map_small': tensor(-1.),
         'mar_1': tensor(0.6000),
         'mar_10': tensor(0.6000),
         'mar_100': tensor(0.6000),
         'mar_100_per_class': tensor(-1.),
         'mar_large': tensor(0.6000),
         'mar_medium': tensor(-1.),
         'mar_small': tensor(-1.)}
    """
    is_differentiable: bool = False
    higher_is_better: Optional[bool] = None
    full_state_update: bool = True

    detections: List[Tensor]
    detection_scores: List[Tensor]
    detection_labels: List[Tensor]
    groundtruths: List[Tensor]
    groundtruth_labels: List[Tensor]

    def __init__(
        self,
        box_format: str = "xyxy",
        iou_type: str = "bbox",
        iou_thresholds: Optional[List[float]] = None,
        rec_thresholds: Optional[List[float]] = None,
        max_detection_thresholds: Optional[List[int]] = None,
        class_metrics: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        if not _TORCHVISION_GREATER_EQUAL_0_8:
            raise ModuleNotFoundError(
                "`MeanAveragePrecision` metric requires that `torchvision` version 0.8.0 or newer is installed."
                " Please install with `pip install torchvision>=0.8` or `pip install torchmetrics[detection]`."
            )

        allowed_box_formats = ("xyxy", "xywh", "cxcywh")
        allowed_iou_types = ("segm", "bbox")
        if box_format not in allowed_box_formats:
            raise ValueError(f"Expected argument `box_format` to be one of {allowed_box_formats} but got {box_format}")
        self.box_format = box_format
        self.iou_thresholds = iou_thresholds or torch.linspace(0.5, 0.95, round((0.95 - 0.5) / 0.05) + 1).tolist()
        self.rec_thresholds = rec_thresholds or torch.linspace(0.0, 1.00, round(1.00 / 0.01) + 1).tolist()
        max_det_thr, _ = torch.sort(IntTensor(max_detection_thresholds or [1, 10, 100]))
        self.max_detection_thresholds = max_det_thr.tolist()
        if iou_type not in allowed_iou_types:
            raise ValueError(f"Expected argument `iou_type` to be one of {allowed_iou_types} but got {iou_type}")
        if iou_type == "segm" and not _PYCOCOTOOLS_AVAILABLE:
            raise ModuleNotFoundError("When `iou_type` is set to 'segm', pycocotools need to be installed")
        self.iou_type = iou_type
        self.bbox_area_ranges = {
            "all": (0**2, int(1e5**2)),
            "small": (0**2, 32**2),
            "medium": (32**2, 96**2),
            "large": (96**2, int(1e5**2)),
        }

        if not isinstance(class_metrics, bool):
            raise ValueError("Expected argument `class_metrics` to be a boolean")

        self.class_metrics = class_metrics
        self.add_state("detections", default=[], dist_reduce_fx=None)
        self.add_state("detection_scores", default=[], dist_reduce_fx=None)
        self.add_state("detection_labels", default=[], dist_reduce_fx=None)
        self.add_state("groundtruths", default=[], dist_reduce_fx=None)
        self.add_state("groundtruth_labels", default=[], dist_reduce_fx=None)

    def update(self, preds: List[Dict[str, Tensor]], target: List[Dict[str, Tensor]]) -> None:  # type: ignore
        """Update state with predictions and targets."""
        _input_validator(preds, target, iou_type=self.iou_type)

        for item in preds:

            detections = self._get_safe_item_values(item)

            self.detections.append(detections)
            self.detection_labels.append(item["labels"])
            self.detection_scores.append(item["scores"])

        for item in target:
            groundtruths = self._get_safe_item_values(item)
            self.groundtruths.append(groundtruths)
            self.groundtruth_labels.append(item["labels"])

    def _move_list_states_to_cpu(self) -> None:
        """Move list states to cpu to save GPU memory."""

        for key in self._defaults.keys():
            current_val = getattr(self, key)
            current_to_cpu = []
            if isinstance(current_val, Sequence):
                for cur_v in current_val:
                    # Cannot handle RLE as Tensor
                    if not isinstance(cur_v, tuple):
                        cur_v = cur_v.to("cpu")
                    current_to_cpu.append(cur_v)
            setattr(self, key, current_to_cpu)

    def _get_safe_item_values(self, item: Dict[str, Any]) -> Union[Tensor, Tuple]:
        if self.iou_type == "bbox":
            boxes = _fix_empty_tensors(item["boxes"])
            if boxes.numel() > 0:
                boxes = box_convert(boxes, in_fmt=self.box_format, out_fmt="xyxy")
            return boxes
        elif self.iou_type == "segm":
            masks = []

            for i in item["masks"].cpu().numpy():
                rle = mask_utils.encode(np.asfortranarray(i))
                masks.append((tuple(rle["size"]), rle["counts"]))

            return tuple(masks)
        else:
            raise Exception(f"IOU type {self.iou_type} is not supported")

    def _get_classes(self) -> List:
        """Returns a list of unique classes found in ground truth and detection data."""
        if len(self.detection_labels) > 0 or len(self.groundtruth_labels) > 0:
            return torch.cat(self.detection_labels + self.groundtruth_labels).unique().tolist()
        return []

    def _compute_iou(self, idx: int, class_id: int, max_det: int) -> Tensor:
        """Computes the Intersection over Union (IoU) for ground truth and detection bounding boxes for the given
        image and class.

        Args:
            idx:
                Image Id, equivalent to the index of supplied samples
            class_id:
                Class Id of the supplied ground truth and detection labels
            max_det:
                Maximum number of evaluated detection bounding boxes
        """

        # if self.iou_type == "bbox":
        gt = self.groundtruths[idx]
        det = self.detections[idx]

        gt_label_mask = (self.groundtruth_labels[idx] == class_id).nonzero().squeeze(1)
        det_label_mask = (self.detection_labels[idx] == class_id).nonzero().squeeze(1)

        if len(gt_label_mask) == 0 or len(det_label_mask) == 0:
            return Tensor([])

        gt = [gt[i] for i in gt_label_mask]
        det = [det[i] for i in det_label_mask]

        if len(gt) == 0 or len(det) == 0:
            return Tensor([])

        # Sort by scores and use only max detections
        scores = self.detection_scores[idx]
        scores_filtered = scores[self.detection_labels[idx] == class_id]
        inds = torch.argsort(scores_filtered, descending=True)

        # TODO Fix (only for masks is necessary)
        det = [det[i] for i in inds]
        if len(det) > max_det:
            det = det[:max_det]

        ious = compute_iou(det, gt, self.iou_type).to(self.device)
        return ious

    def __evaluate_image_gt_no_preds(
        self, gt: Tensor, gt_label_mask: Tensor, area_range: Tuple[int, int], nb_iou_thrs: int
    ) -> Dict[str, Any]:
        """Some GT but no predictions."""
        # GTs
        gt = [gt[i] for i in gt_label_mask]
        nb_gt = len(gt)
        areas = compute_area(gt, iou_type=self.iou_type).to(self.device)
        ignore_area = (areas < area_range[0]) | (areas > area_range[1])
        gt_ignore, _ = torch.sort(ignore_area.to(torch.uint8))
        gt_ignore = gt_ignore.to(torch.bool)

        # Detections
        nb_det = 0
        det_ignore = torch.zeros((nb_iou_thrs, nb_det), dtype=torch.bool, device=self.device)

        return {
            "dtMatches": torch.zeros((nb_iou_thrs, nb_det), dtype=torch.bool, device=self.device),
            "gtMatches": torch.zeros((nb_iou_thrs, nb_gt), dtype=torch.bool, device=self.device),
            "dtScores": torch.zeros(nb_det, dtype=torch.float32, device=self.device),
            "gtIgnore": gt_ignore,
            "dtIgnore": det_ignore,
        }

    def __evaluate_image_preds_no_gt(
        self, det: Tensor, idx: int, det_label_mask: Tensor, max_det: int, area_range: Tuple[int, int], nb_iou_thrs: int
    ) -> Dict[str, Any]:
        """Some predictions but no GT."""
        # GTs
        nb_gt = 0

        gt_ignore = torch.zeros(nb_gt, dtype=torch.bool, device=self.device)

        # Detections

        det = [det[i] for i in det_label_mask]
        scores = self.detection_scores[idx]
        scores_filtered = scores[det_label_mask]
        scores_sorted, dtind = torch.sort(scores_filtered, descending=True)

        det = [det[i] for i in dtind]
        if len(det) > max_det:
            det = det[:max_det]
        nb_det = len(det)
        det_areas = compute_area(det, iou_type=self.iou_type).to(self.device)
        det_ignore_area = (det_areas < area_range[0]) | (det_areas > area_range[1])
        ar = det_ignore_area.reshape((1, nb_det))
        det_ignore = torch.repeat_interleave(ar, nb_iou_thrs, 0)

        return {
            "dtMatches": torch.zeros((nb_iou_thrs, nb_det), dtype=torch.bool, device=self.device),
            "gtMatches": torch.zeros((nb_iou_thrs, nb_gt), dtype=torch.bool, device=self.device),
            "dtScores": scores_sorted.to(self.device),
            "gtIgnore": gt_ignore.to(self.device),
            "dtIgnore": det_ignore.to(self.device),
        }

    def _evaluate_image(
        self, idx: int, class_id: int, area_range: Tuple[int, int], max_det: int, ious: dict
    ) -> Optional[dict]:
        """Perform evaluation for single class and image.

        Args:
            idx:
                Image Id, equivalent to the index of supplied samples.
            class_id:
                Class Id of the supplied ground truth and detection labels.
            area_range:
                List of lower and upper bounding box area threshold.
            max_det:
                Maximum number of evaluated detection bounding boxes.
            ious:
                IoU results for image and class.
        """

        gt = self.groundtruths[idx]
        det = self.detections[idx]
        gt_label_mask = (self.groundtruth_labels[idx] == class_id).nonzero().squeeze(1)
        det_label_mask = (self.detection_labels[idx] == class_id).nonzero().squeeze(1)

        # No Gt and No predictions --> ignore image
        if len(gt_label_mask) == 0 and len(det_label_mask) == 0:
            return None

        nb_iou_thrs = len(self.iou_thresholds)

        # Some GT but no predictions
        if len(gt_label_mask) > 0 and len(det_label_mask) == 0:
            return self.__evaluate_image_gt_no_preds(gt, gt_label_mask, area_range, nb_iou_thrs)

        # Some predictions but no GT
        if len(gt_label_mask) == 0 and len(det_label_mask) >= 0:
            return self.__evaluate_image_preds_no_gt(det, idx, det_label_mask, max_det, area_range, nb_iou_thrs)

        gt = [gt[i] for i in gt_label_mask]
        det = [det[i] for i in det_label_mask]
        if len(gt) == 0 and len(det) == 0:
            return None
        if isinstance(det, dict):
            det = [det]
        if isinstance(gt, dict):
            gt = [gt]

        areas = compute_area(gt, iou_type=self.iou_type).to(self.device)

        ignore_area = torch.logical_or(areas < area_range[0], areas > area_range[1])

        # sort dt highest score first, sort gt ignore last
        ignore_area_sorted, gtind = torch.sort(ignore_area.to(torch.uint8))
        # Convert to uint8 temporarily and back to bool, because "Sort currently does not support bool dtype on CUDA"

        ignore_area_sorted = ignore_area_sorted.to(torch.bool).to(self.device)

        gt = [gt[i] for i in gtind]
        scores = self.detection_scores[idx]
        scores_filtered = scores[det_label_mask]
        scores_sorted, dtind = torch.sort(scores_filtered, descending=True)
        det = [det[i] for i in dtind]
        if len(det) > max_det:
            det = det[:max_det]
        # load computed ious
        ious = ious[idx, class_id][:, gtind] if len(ious[idx, class_id]) > 0 else ious[idx, class_id]

        nb_iou_thrs = len(self.iou_thresholds)
        nb_gt = len(gt)
        nb_det = len(det)
        gt_matches = torch.zeros((nb_iou_thrs, nb_gt), dtype=torch.bool, device=self.device)
        det_matches = torch.zeros((nb_iou_thrs, nb_det), dtype=torch.bool, device=self.device)
        gt_ignore = ignore_area_sorted
        det_ignore = torch.zeros((nb_iou_thrs, nb_det), dtype=torch.bool, device=self.device)

        if torch.numel(ious) > 0:
            for idx_iou, t in enumerate(self.iou_thresholds):
                for idx_det, _ in enumerate(det):
                    m = MeanAveragePrecision._find_best_gt_match(t, gt_matches, idx_iou, gt_ignore, ious, idx_det)
                    if m == -1:
                        continue
                    det_ignore[idx_iou, idx_det] = gt_ignore[m]
                    det_matches[idx_iou, idx_det] = 1
                    gt_matches[idx_iou, m] = 1

        # set unmatched detections outside of area range to ignore
        det_areas = compute_area(det, iou_type=self.iou_type).to(self.device)
        det_ignore_area = (det_areas < area_range[0]) | (det_areas > area_range[1])
        ar = det_ignore_area.reshape((1, nb_det))
        det_ignore = torch.logical_or(
            det_ignore, torch.logical_and(det_matches == 0, torch.repeat_interleave(ar, nb_iou_thrs, 0))
        )

        return {
            "dtMatches": det_matches.to(self.device),
            "gtMatches": gt_matches.to(self.device),
            "dtScores": scores_sorted.to(self.device),
            "gtIgnore": gt_ignore.to(self.device),
            "dtIgnore": det_ignore.to(self.device),
        }

    @staticmethod
    def _find_best_gt_match(
        thr: int, gt_matches: Tensor, idx_iou: float, gt_ignore: Tensor, ious: Tensor, idx_det: int
    ) -> int:
        """Return id of best ground truth match with current detection.

        Args:
            thr:
                Current threshold value.
            gt_matches:
                Tensor showing if a ground truth matches for threshold ``t`` exists.
            idx_iou:
                Id of threshold ``t``.
            gt_ignore:
                Tensor showing if ground truth should be ignored.
            ious:
                IoUs for all combinations of detection and ground truth.
            idx_det:
                Id of current detection.
        """
        previously_matched = gt_matches[idx_iou]
        # Remove previously matched or ignored gts
        remove_mask = previously_matched | gt_ignore
        gt_ious = ious[idx_det] * ~remove_mask
        match_idx = gt_ious.argmax().item()
        if gt_ious[match_idx] > thr:
            return match_idx
        return -1

    def _summarize(
        self,
        results: Dict,
        avg_prec: bool = True,
        iou_threshold: Optional[float] = None,
        area_range: str = "all",
        max_dets: int = 100,
    ) -> Tensor:
        """Perform evaluation for single class and image.

        Args:
            results:
                Dictionary including precision, recall and scores for all combinations.
            avg_prec:
                Calculate average precision. Else calculate average recall.
            iou_threshold:
                IoU threshold. If set to ``None`` it all values are used. Else results are filtered.
            area_range:
                Bounding box area range key.
            max_dets:
                Maximum detections.
        """
        area_inds = [i for i, k in enumerate(self.bbox_area_ranges.keys()) if k == area_range]
        mdet_inds = [i for i, k in enumerate(self.max_detection_thresholds) if k == max_dets]
        if avg_prec:
            # dimension of precision: [TxRxKxAxM]
            prec = results["precision"]
            # IoU
            if iou_threshold is not None:
                thr = self.iou_thresholds.index(iou_threshold)
                prec = prec[thr, :, :, area_inds, mdet_inds]
            else:
                prec = prec[:, :, :, area_inds, mdet_inds]
        else:
            # dimension of recall: [TxKxAxM]
            prec = results["recall"]
            if iou_threshold is not None:
                thr = self.iou_thresholds.index(iou_threshold)
                prec = prec[thr, :, :, area_inds, mdet_inds]
            else:
                prec = prec[:, :, area_inds, mdet_inds]

        mean_prec = torch.tensor([-1.0]) if len(prec[prec > -1]) == 0 else torch.mean(prec[prec > -1])
        return mean_prec

    def _calculate(self, class_ids: List) -> Tuple[MAPMetricResults, MARMetricResults]:
        """Calculate the precision and recall for all supplied classes to calculate mAP/mAR.

        Args:
            class_ids:
                List of label class Ids.
        """
        img_ids = range(len(self.groundtruths))
        max_detections = self.max_detection_thresholds[-1]
        area_ranges = self.bbox_area_ranges.values()

        ious = {
            (idx, class_id): self._compute_iou(idx, class_id, max_detections)
            for idx in img_ids
            for class_id in class_ids
        }

        eval_imgs = [
            self._evaluate_image(img_id, class_id, area, max_detections, ious)
            for class_id in class_ids
            for area in area_ranges
            for img_id in img_ids
        ]

        nb_iou_thrs = len(self.iou_thresholds)
        nb_rec_thrs = len(self.rec_thresholds)
        nb_classes = len(class_ids)
        nb_bbox_areas = len(self.bbox_area_ranges)
        nb_max_det_thrs = len(self.max_detection_thresholds)
        nb_imgs = len(img_ids)
        precision = -torch.ones((nb_iou_thrs, nb_rec_thrs, nb_classes, nb_bbox_areas, nb_max_det_thrs))
        recall = -torch.ones((nb_iou_thrs, nb_classes, nb_bbox_areas, nb_max_det_thrs))
        scores = -torch.ones((nb_iou_thrs, nb_rec_thrs, nb_classes, nb_bbox_areas, nb_max_det_thrs))

        # move tensors if necessary
        rec_thresholds_tensor = torch.tensor(self.rec_thresholds)

        # retrieve E at each category, area range, and max number of detections
        for idx_cls, _ in enumerate(class_ids):
            for idx_bbox_area, _ in enumerate(self.bbox_area_ranges):
                for idx_max_det_thrs, max_det in enumerate(self.max_detection_thresholds):
                    recall, precision, scores = MeanAveragePrecision.__calculate_recall_precision_scores(
                        recall,
                        precision,
                        scores,
                        idx_cls=idx_cls,
                        idx_bbox_area=idx_bbox_area,
                        idx_max_det_thrs=idx_max_det_thrs,
                        eval_imgs=eval_imgs,
                        rec_thresholds=rec_thresholds_tensor,
                        max_det=max_det,
                        nb_imgs=nb_imgs,
                        nb_bbox_areas=nb_bbox_areas,
                    )

        return precision, recall

    def _summarize_results(self, precisions: Tensor, recalls: Tensor) -> Tuple[MAPMetricResults, MARMetricResults]:
        """Summarizes the precision and recall values to calculate mAP/mAR.

        Args:
            precisions:
                Precision values for different thresholds
            recalls:
                Recall values for different thresholds
        """
        results = dict(precision=precisions, recall=recalls)
        map_metrics = MAPMetricResults()
        map_metrics.map = self._summarize(results, True)
        last_max_det_thr = self.max_detection_thresholds[-1]
        if 0.5 in self.iou_thresholds:
            map_metrics.map_50 = self._summarize(results, True, iou_threshold=0.5, max_dets=last_max_det_thr)
        else:
            map_metrics.map_50 = torch.tensor([-1])
        if 0.75 in self.iou_thresholds:
            map_metrics.map_75 = self._summarize(results, True, iou_threshold=0.75, max_dets=last_max_det_thr)
        else:
            map_metrics.map_75 = torch.tensor([-1])
        map_metrics.map_small = self._summarize(results, True, area_range="small", max_dets=last_max_det_thr)
        map_metrics.map_medium = self._summarize(results, True, area_range="medium", max_dets=last_max_det_thr)
        map_metrics.map_large = self._summarize(results, True, area_range="large", max_dets=last_max_det_thr)

        mar_metrics = MARMetricResults()
        for max_det in self.max_detection_thresholds:
            mar_metrics[f"mar_{max_det}"] = self._summarize(results, False, max_dets=max_det)
        mar_metrics.mar_small = self._summarize(results, False, area_range="small", max_dets=last_max_det_thr)
        mar_metrics.mar_medium = self._summarize(results, False, area_range="medium", max_dets=last_max_det_thr)
        mar_metrics.mar_large = self._summarize(results, False, area_range="large", max_dets=last_max_det_thr)

        return map_metrics, mar_metrics

    @staticmethod
    def __calculate_recall_precision_scores(
        recall: Tensor,
        precision: Tensor,
        scores: Tensor,
        idx_cls: int,
        idx_bbox_area: int,
        idx_max_det_thrs: int,
        eval_imgs: list,
        rec_thresholds: Tensor,
        max_det: int,
        nb_imgs: int,
        nb_bbox_areas: int,
    ) -> Tuple[Tensor, Tensor, Tensor]:
        nb_rec_thrs = len(rec_thresholds)
        idx_cls_pointer = idx_cls * nb_bbox_areas * nb_imgs
        idx_bbox_area_pointer = idx_bbox_area * nb_imgs
        # Load all image evals for current class_id and area_range
        img_eval_cls_bbox = [eval_imgs[idx_cls_pointer + idx_bbox_area_pointer + i] for i in range(nb_imgs)]
        img_eval_cls_bbox = [e for e in img_eval_cls_bbox if e is not None]
        if not img_eval_cls_bbox:
            return recall, precision, scores

        det_scores = torch.cat([e["dtScores"][:max_det] for e in img_eval_cls_bbox])

        # different sorting method generates slightly different results.
        # mergesort is used to be consistent as Matlab implementation.
        # Sort in PyTorch does not support bool types on CUDA (yet, 1.11.0)
        dtype = torch.uint8 if det_scores.is_cuda and det_scores.dtype is torch.bool else det_scores.dtype
        # Explicitly cast to uint8 to avoid error for bool inputs on CUDA to argsort
        inds = torch.argsort(det_scores.to(dtype), descending=True)
        det_scores_sorted = det_scores[inds]

        det_matches = torch.cat([e["dtMatches"][:, :max_det] for e in img_eval_cls_bbox], axis=1)[:, inds]
        det_ignore = torch.cat([e["dtIgnore"][:, :max_det] for e in img_eval_cls_bbox], axis=1)[:, inds]
        gt_ignore = torch.cat([e["gtIgnore"] for e in img_eval_cls_bbox])
        npig = torch.count_nonzero(gt_ignore == False)  # noqa: E712
        if npig == 0:
            return recall, precision, scores
        tps = torch.logical_and(det_matches, torch.logical_not(det_ignore))
        fps = torch.logical_and(torch.logical_not(det_matches), torch.logical_not(det_ignore))

        tp_sum = torch.cumsum(tps, axis=1, dtype=torch.float)
        fp_sum = torch.cumsum(fps, axis=1, dtype=torch.float)
        for idx, (tp, fp) in enumerate(zip(tp_sum, fp_sum)):
            nd = len(tp)
            rc = tp / npig
            pr = tp / (fp + tp + torch.finfo(torch.float64).eps)
            prec = torch.zeros((nb_rec_thrs,))
            score = torch.zeros((nb_rec_thrs,))

            recall[idx, idx_cls, idx_bbox_area, idx_max_det_thrs] = rc[-1] if nd else 0

            # Remove zigzags for AUC
            diff_zero = torch.zeros((1,), device=pr.device)
            diff = torch.ones((1,), device=pr.device)
            while not torch.all(diff == 0):

                diff = torch.clamp(torch.cat(((pr[1:] - pr[:-1]), diff_zero), 0), min=0)
                pr += diff

            inds = torch.searchsorted(rc, rec_thresholds.to(rc.device), right=False)
            num_inds = inds.argmax() if inds.max() >= nd else nb_rec_thrs
            inds = inds[:num_inds]
            prec[:num_inds] = pr[inds]
            score[:num_inds] = det_scores_sorted[inds]
            precision[idx, :, idx_cls, idx_bbox_area, idx_max_det_thrs] = prec
            scores[idx, :, idx_cls, idx_bbox_area, idx_max_det_thrs] = score

        return recall, precision, scores

    def compute(self) -> dict:
        """Computes metric."""
        classes = self._get_classes()
        precisions, recalls = self._calculate(classes)
        map_val, mar_val = self._summarize_results(precisions, recalls)

        # if class mode is enabled, evaluate metrics per class
        map_per_class_values: Tensor = torch.tensor([-1.0])
        mar_max_dets_per_class_values: Tensor = torch.tensor([-1.0])
        if self.class_metrics:
            map_per_class_list = []
            mar_max_dets_per_class_list = []

            for class_idx, _ in enumerate(classes):
                cls_precisions = precisions[:, :, class_idx].unsqueeze(dim=2)
                cls_recalls = recalls[:, class_idx].unsqueeze(dim=1)
                cls_map, cls_mar = self._summarize_results(cls_precisions, cls_recalls)
                map_per_class_list.append(cls_map.map)
                mar_max_dets_per_class_list.append(cls_mar[f"mar_{self.max_detection_thresholds[-1]}"])

            map_per_class_values = torch.tensor(map_per_class_list, dtype=torch.float)
            mar_max_dets_per_class_values = torch.tensor(mar_max_dets_per_class_list, dtype=torch.float)

        metrics = COCOMetricResults()
        metrics.update(map_val)
        metrics.update(mar_val)
        metrics.map_per_class = map_per_class_values
        metrics[f"mar_{self.max_detection_thresholds[-1]}_per_class"] = mar_max_dets_per_class_values

        return metrics
