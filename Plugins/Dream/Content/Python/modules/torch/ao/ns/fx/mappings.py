import operator

import torch
import torch.nn as nn
import torch.nn.functional as F
toq = torch.ops.quantized

import torch.nn.quantized as nnq
import torch.nn.quantized.dynamic as nnqd
import torch.nn.intrinsic.quantized as nniq
import torch.nn.intrinsic.quantized.dynamic as nniqd
import torch.nn.intrinsic.qat as nniqat
import torch.nn.intrinsic as nni
import torch.nn.qat as nnqat
import torch.nn.qat.dynamic as nnqatd
from torch.ao.quantization.backend_config import get_native_backend_config_dict
import torch.ao.quantization.fx._lower_to_native_backend as \
    _lower_to_native_backend
import torch.ao.quantization.quantization_mappings as quantization_mappings

from .ns_types import NSNodeTargetType

from typing import Set, Dict, List, Optional


def get_base_name_to_sets_of_related_ops() -> Dict[str, Set[NSNodeTargetType]]:
    # note: this set is modified below by items from backend_config_dict
    sets_of_related_ops: List[Set[NSNodeTargetType]] = [
        # conv modules
        set([
            nn.Conv1d,
        ]),
        set([
            nn.Conv2d,
        ]),
        set([
            nn.Conv3d,
        ]),
        # conv functionals
        set([
            F.conv1d,
        ]),
        set([
            F.conv2d,
        ]),
        set([
            F.conv3d,
        ]),
        # linear modules
        set([
            nn.Linear,
        ]),
        # linear functionals
        set([
            F.linear,
        ]),
        # average pool
        set([
            nn.AvgPool1d,
            torch.avg_pool1d,
        ]),
        set([
            nn.AvgPool2d,
            torch._C._nn.avg_pool2d,
        ]),
        set([
            nn.AvgPool3d,
            torch._C._nn.avg_pool3d,
        ]),
        # adaptive average pool
        set([
            nn.AdaptiveAvgPool1d,
            F.adaptive_avg_pool1d,
        ]),
        set([
            nn.AdaptiveAvgPool2d,
            F.adaptive_avg_pool2d,
        ]),
        set([
            nn.AdaptiveAvgPool3d,
            F.adaptive_avg_pool3d,
        ]),
        # LSTM
        set([
            nn.LSTM,
        ]),
        # add
        set([
            torch.add,
            operator.add,  # x + y
        ]),
        # cat
        set([
            torch.cat,
        ]),
        # mul
        set([
            torch.mul,
            operator.mul,
        ]),
        # relu
        set([
            F.relu,
            nn.ReLU,
            'relu',
            'relu_',
            torch.relu,
        ]),
        # maxpool
        set([
            nn.MaxPool1d,
            F.max_pool1d,
        ]),
        set([
            nn.MaxPool2d,
            F.max_pool2d,
        ]),
        set([
            nn.MaxPool3d,
            F.max_pool3d,
        ]),
        # sigmoid
        set([
            torch.sigmoid,
            'sigmoid',
            'sigmoid_',
            nn.Sigmoid,
            F.sigmoid,
        ]),
        # BatchNorm
        set([
            nn.BatchNorm2d,
        ]),
        set([
            nn.BatchNorm3d,
        ]),
        # ConvTranspose
        set([
            nn.ConvTranspose1d,
        ]),
        set([
            nn.ConvTranspose2d,
        ]),
        set([
            nn.ConvTranspose3d,
        ]),
        # ELU
        set([
            nn.ELU,
        ]),
        # Embedding
        set([
            nn.Embedding,
        ]),
        # EmbeddingBag
        set([
            nn.EmbeddingBag,
        ]),
        # GroupNorm
        set([
            nn.GroupNorm,
        ]),
        # Hardswish
        set([
            nn.Hardswish,
        ]),
        # InstanceNorm
        set([
            nn.InstanceNorm1d,
        ]),
        set([
            nn.InstanceNorm2d,
        ]),
        set([
            nn.InstanceNorm3d,
        ]),
        # LayerNorm
        set([
            nn.LayerNorm,
        ]),
        # LeakyReLU
        set([
            nn.LeakyReLU,
        ]),
        # ReLU6
        set([
            nn.ReLU6,
            F.relu6,
        ]),
        # F.elu
        set([
            F.elu,
        ]),
        # F.hardswish
        set([
            F.hardswish,
        ]),
        # F.instance_norm
        set([
            F.instance_norm,
        ]),
        # F.layer_norm
        set([
            F.layer_norm,
        ]),
        # F.leaky_relu
        set([
            F.leaky_relu,
        ]),
        # F.silu
        set([
            nn.SiLU,
            F.silu,
        ]),
        # F.mish
        set([
            nn.Mish,
            F.mish,
        ]),
        # F.tanh
        set([
            nn.Tanh,
            F.tanh,
            torch.tanh,
            'tanh_',
            'tanh',
        ]),
        # F.hardsigmoid
        set([
            'hardsigmoid_',
            'hardsigmoid',
            F.hardsigmoid,
            nn.Hardsigmoid,
        ]),
        # F.hardtanh
        set([
            nn.Hardtanh,
            F.hardtanh,
            F.hardtanh_,
        ]),
        # floordiv
        set([
            operator.floordiv,
        ]),
        # unsqueeze
        set([
            torch.unsqueeze,
        ]),
        # stack
        set([
            torch.stack,
        ]),
        # squeeze
        set([
            torch.squeeze,
        ]),
        # sort
        set([
            torch.sort,
        ]),
        # repeat_interleave
        set([
            torch.repeat_interleave,
        ]),
        # min
        set([
            torch.min,
        ]),
        # mean
        set([
            torch.mean,
        ]),
        # max
        set([
            torch.max,
        ]),
        # transpose
        set([
            torch.transpose,
        ]),
        # flatten
        set([
            torch.flatten,
        ]),
        # clamp
        set([
            torch.clamp,
        ]),
        # chunk
        set([
            torch.chunk,
        ]),
        # interpolate
        set([
            torch.nn.functional.interpolate,
        ]),
        # dropout
        set([
            nn.Dropout,
        ]),
        # F.dropout
        set([
            F.dropout,
        ]),
        # matmul
        set([
            torch.matmul,
        ]),
        # Softmax
        set([
            nn.Softmax,
        ]),
    ]

    # for each floating point op, add versions of the op added by
    # backend_config_dict
    backend_config_dict = get_native_backend_config_dict()

    new_connections = [
        # technical debt edge case
        (nn.Linear, nn.modules.linear.NonDynamicallyQuantizableLinear),
    ]

    for config in backend_config_dict['configs']:

        if 'pattern' not in config:
            continue

        # format: (c, (b, a))
        pattern = config['pattern']
        first_element = pattern
        # look from the end, because pattern is in reverse order
        while isinstance(first_element, (list, tuple)):
            first_element = first_element[-1]

        if 'fused_module' in config:
            # case 1: pattern fuses a pattern of ops into an op
            # example: nn.Conv1d, nn.ReLU fused into nni.ConvReLU1d
            new_connections.append((first_element, config['fused_module']))

        if 'qat_module' in config:
            # case 2: pattern swaps a module into a QAT module
            # example: nni.ConvReLU1d swapped into nniqat.ConvReLU1d
            new_connections.append((first_element, config['qat_module']))

        if 'reference_quantized_module_for_root' in config:
            # case 3: reference version of floating point module, such as
            # nn.Conv2d and nnqr.Conv2d
            new_connections.append(
                (first_element, config['reference_quantized_module_for_root'])
            )

    #
    # Add reference module swaps from default lowering path
    #

    for source_to_target in (
        _lower_to_native_backend.STATIC_LOWER_MODULE_MAP,
        _lower_to_native_backend.DYNAMIC_LOWER_MODULE_MAP,
        _lower_to_native_backend.WEIGHT_ONLY_LOWER_MODULE_MAP,
        _lower_to_native_backend.SPECIAL_PATTERN_LOWER_MODULE_MAP,
    ):
        for source, target in source_to_target.items():  # type: ignore[attr-defined]
            new_connections.append((source, target))

    for source_to_double_target in (
        _lower_to_native_backend.STATIC_LOWER_FUSED_MODULE_MAP,
        _lower_to_native_backend.DYNAMIC_LOWER_FUSED_MODULE_MAP,
    ):
        for source, (target1, target2) in source_to_double_target.items():  # type: ignore[attr-defined]
            new_connections.append((source, target1))
            new_connections.append((source, target2))

    #
    # Add function swaps from default lowering path
    #

    for source, (target1, target2) in \
            _lower_to_native_backend.STATIC_LOWER_FUNCTIONAL_MAP.items():
        new_connections.append((source, target1))
        new_connections.append((source, target2))

    for source_to_target in (
        _lower_to_native_backend.QBIN_OP_MAPPING,
        _lower_to_native_backend.QBIN_RELU_OP_MAPPING,
        quantization_mappings.DEFAULT_FLOAT_TO_QUANTIZED_OPERATOR_MAPPINGS,
    ):
        for source, target in source_to_target.items():
            new_connections.append((source, target))

    #
    # Add other swaps, ideally in the future this could be removed
    # after the lowering code stops using these.
    #
    for source_to_target in (
        quantization_mappings.DEFAULT_DYNAMIC_QUANT_MODULE_MAPPINGS,
    ):
        for source, target in source_to_target.items():
            new_connections.append((source, target))


    # add the new connections from backend_config_dict
    for item1, item2 in new_connections:
        for set_of_related_ops in sets_of_related_ops:
            if item1 in set_of_related_ops or item2 in set_of_related_ops:
                set_of_related_ops.add(item1)
                set_of_related_ops.add(item2)
                break

    base_name_to_sets_of_related_ops: Dict[str, Set[NSNodeTargetType]] = {}

    counter = 0
    for set_of_related_ops in sets_of_related_ops:
        base_name = str(counter)
        counter += 1
        base_name_to_sets_of_related_ops[base_name] = set_of_related_ops

    return base_name_to_sets_of_related_ops


def get_base_name_for_op(
    base_name_to_sets_of_related_ops: Dict[str, Set[NSNodeTargetType]],
    op: NSNodeTargetType,
) -> Optional[str]:
    for base_name, set_of_related_ops in base_name_to_sets_of_related_ops.items():
        if op in set_of_related_ops:
            return base_name
    return None


def add_op_to_sets_of_related_ops(
    base_name_to_sets_of_related_ops: Dict[str, Set[NSNodeTargetType]],
    op: NSNodeTargetType,
    related_op: Optional[NSNodeTargetType],
) -> None:
    if related_op is not None:
        for base_name, set_of_related_ops in base_name_to_sets_of_related_ops.items():
            if related_op in set_of_related_ops:
                set_of_related_ops.add(op)
                return
        # if we got here, related_op was not found
        raise AssertionError(f"{related_op} was not found")
    else:
        counter = 0
        while str(counter) in base_name_to_sets_of_related_ops:
            counter += 1
        base_name_to_sets_of_related_ops[str(counter)] = set([op])


# TODO(future PR): clean this up
def get_node_type_to_io_type_map() -> Dict[str, Set[NSNodeTargetType]]:
    FUNS_IO_TYPE_FP32: Set[NSNodeTargetType] = set([
        F.linear,
        F.conv1d,
        F.conv2d,
        F.conv3d,
        torch.cat,
        F.elu,
        F.hardswish,
        F.instance_norm,
        F.layer_norm,
        F.leaky_relu,
        F.dropout,
        F.silu,
        F.mish,
        operator.add,
        torch.add,
        operator.mul,
        torch.mul,
        torch.sum,
    ])

    FUNS_IO_TYPE_FP16: Set[NSNodeTargetType] = set()

    FUNS_IO_TYPE_INT8: Set[NSNodeTargetType] = set([
        toq.linear,
        toq.linear_relu,
        toq.conv1d,
        toq.conv1d_relu,
        toq.conv2d,
        toq.conv2d_relu,
        toq.conv3d,
        toq.conv3d_relu,
        toq.cat,
        toq.elu,
        toq.hardswish,
        toq.instance_norm,
        toq.layer_norm,
        toq.leaky_relu,
        toq.dropout,
        # TODO(future PR): implement shadowing for binary ops and
        # uncomment below
        # toq.add,
        # toq.mul,
    ])

    FUNS_IO_TYPE_FP32_OR_INT8: Set[NSNodeTargetType] = set([
        F.relu,
        F.tanh,
        torch.tanh,
        F.sigmoid,
        torch.sigmoid,
        F.hardsigmoid,
        operator.floordiv,
        torch.adaptive_avg_pool1d,
        F.adaptive_avg_pool2d,
        F.adaptive_avg_pool3d,
        F.dropout,
        F.hardtanh,
        F.hardtanh_,
        F.interpolate,
        F.max_pool1d,
        F.max_pool2d,
        F.max_pool3d,
        F.relu6,
        torch.avg_pool1d,
        torch._C._nn.avg_pool2d,
        torch._C._nn.avg_pool3d,
        torch.cat,
        torch.chunk,
        torch.clamp,
        torch.flatten,
        torch.transpose,
        torch.max,
        torch.mean,
        torch.min,
        torch.repeat_interleave,
        torch.sort,
        torch.squeeze,
        torch.stack,
        torch.unsqueeze,
        operator.add,
    ])

    MODS_IO_TYPE_FP32: Set[NSNodeTargetType] = set([
        nn.Linear,
        nnqat.Linear,
        nnqatd.Linear,
        nnqd.Linear,
        torch.nn.modules.linear.NonDynamicallyQuantizableLinear,
        nn.Conv1d,
        nn.Conv2d,
        nn.Conv3d,
        nnqat.Conv1d,
        nnqat.Conv2d,
        nnqat.Conv3d,
        nnqat.Embedding,
        nnqat.EmbeddingBag,
        nn.LSTM,
        # note: nnqd.Linear is an instance of nnq.Linear, so this
        # check has to happen before the int8 module check
        nnqd.LSTM,
        nn.BatchNorm2d,
        nn.BatchNorm3d,
        nn.Dropout,
        nn.ConvTranspose1d,
        nn.ConvTranspose2d,
        nn.ConvTranspose3d,
        nn.ELU,
        nn.GroupNorm,
        nn.InstanceNorm1d,
        nn.InstanceNorm2d,
        nn.InstanceNorm3d,
        nn.LayerNorm,
        nn.Hardswish,
        nn.LeakyReLU,
        nn.ReLU6,
        nn.SiLU,
        nn.Mish,
        nn.Softmax,
        nni.BNReLU2d,
        nni.BNReLU3d,
        nni.ConvReLU1d,
        nni.ConvReLU2d,
        nni.ConvReLU3d,
        nni.LinearReLU,
        nni.LinearBn1d,
        nni.ConvBn1d,
        nni.ConvBn2d,
        nni.ConvBn3d,
        nniqat.ConvBn1d,
        nniqat.ConvBn2d,
        nniqat.ConvBn3d,
        nniqat.ConvBnReLU1d,
        nniqat.ConvBnReLU2d,
        nniqat.ConvBnReLU3d,
        nniqat.ConvReLU1d,
        nniqat.ConvReLU2d,
        nniqat.ConvReLU3d,
        nniqat.LinearReLU,
        nniqat.LinearBn1d,
        nniqd.LinearReLU,
    ])

    MODS_IO_TYPE_INT8: Set[NSNodeTargetType] = set([
        nnq.Linear,
        nnq.Conv1d,
        nnq.Conv2d,
        nnq.Conv3d,
        nnq.BatchNorm2d,
        nnq.BatchNorm3d,
        nnq.Dropout,
        nnq.ConvTranspose1d,
        nnq.ConvTranspose2d,
        nnq.ELU,
        nnq.InstanceNorm1d,
        nnq.InstanceNorm2d,
        nnq.InstanceNorm3d,
        nnq.LayerNorm,
        nnq.Hardswish,
        nnq.LeakyReLU,
        nnq.Embedding,
        nnq.EmbeddingBag,
        nnq.Dropout,
        nnq.Softmax,
        nniq.BNReLU2d,
        nniq.BNReLU3d,
        nniq.ConvReLU1d,
        nniq.ConvReLU2d,
        nniq.ConvReLU3d,
        nniq.LinearReLU,
    ])

    MODS_IO_TYPE_FP32_OR_INT8: Set[NSNodeTargetType] = set([
        nn.ReLU,
        nn.Tanh,
        nn.Sigmoid,
        nn.Hardsigmoid,
        nn.AdaptiveAvgPool1d,
        nn.AdaptiveAvgPool2d,
        nn.AdaptiveAvgPool3d,
        nn.AvgPool1d,
        nn.AvgPool2d,
        nn.AvgPool3d,
        nn.Dropout,
        nn.Hardtanh,
        nn.Identity,
        nn.MaxPool1d,
        nn.MaxPool2d,
        nn.MaxPool3d,
        nn.ReLU6,
    ])

    METHS_IO_TYPE_FP32_OR_INT8: Set[NSNodeTargetType] = set([
        'sigmoid_',
        'sigmoid',
        'tanh_',
        'tanh',
        'hardsigmoid_',
        'hardsigmoid',
        'relu_',
        'relu',
    ])

    return {
        'funs_io_type_fp32': FUNS_IO_TYPE_FP32,
        'funs_io_type_fp16': FUNS_IO_TYPE_FP16,
        'funs_io_type_int8': FUNS_IO_TYPE_INT8,
        'funs_io_type_fp32_or_int8': FUNS_IO_TYPE_FP32_OR_INT8,
        'mods_io_type_fp32': MODS_IO_TYPE_FP32,
        'mods_io_type_int8': MODS_IO_TYPE_INT8,
        'mods_io_type_fp32_or_int8': MODS_IO_TYPE_FP32_OR_INT8,
        'meths_io_type_fp32_or_int8': METHS_IO_TYPE_FP32_OR_INT8,
    }


def get_unmatchable_types_map() -> Dict[str, Set[NSNodeTargetType]]:

    FUNS_UNMATCHABLE: Set[NSNodeTargetType] = set([
        torch.quantize_per_tensor,
        operator.getitem,
    ])

    MODS_UNMATCHABLE: Set[NSNodeTargetType] = set([
        nn.Identity,
    ])

    METHS_UNMATCHABLE: Set[NSNodeTargetType] = set([
        'to',
        'dequantize',
        'reshape',
        'view',
        'unsqueeze_',
        'unsqueeze',
        'transpose',
        'squeeze_',
        'squeeze',
        'size',
        'shape',
        'resize_',
        'repeat_interleave',
        'repeat',
        'permute',
        'numel',
        'mean',
        'detach_',
        'detach',
        'contiguous',
        'clamp',
        'chunk',
    ])

    return {
        'funs_unmatchable': FUNS_UNMATCHABLE,
        'mods_unmatchable': MODS_UNMATCHABLE,
        'meths_unmatchable': METHS_UNMATCHABLE,
    }
