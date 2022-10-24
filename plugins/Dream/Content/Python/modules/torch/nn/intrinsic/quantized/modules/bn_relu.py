
import torch
import torch.nn.intrinsic
import torch.nn.intrinsic.qat
import torch.nn.quantized as nnq


class BNReLU2d(nnq.BatchNorm2d):
    r"""
    A BNReLU2d module is a fused module of BatchNorm2d and ReLU

    We adopt the same interface as :class:`torch.nn.quantized.BatchNorm2d`.

    Attributes:
        Same as torch.nn.quantized.BatchNorm2d

    """
    _FLOAT_MODULE = torch.nn.intrinsic.BNReLU2d

    def __init__(self, num_features, eps=1e-5, momentum=0.1, device=None, dtype=None):
        super(BNReLU2d, self).__init__(num_features, eps=eps, momentum=momentum, device=device, dtype=dtype)

    def forward(self, input):
        # Temporarily using len(shape) instead of ndim due to JIT issue
        # https://github.com/pytorch/pytorch/issues/23890
        if len(input.shape) != 4:
            raise ValueError("Input shape must be `(N, C, H, W)`!")
        return torch.ops.quantized.batch_norm2d_relu(
            input, self.weight, self.bias, self.running_mean,
            self.running_var, self.eps, self.scale, self.zero_point)

    def _get_name(self):
        return 'QuantizedBNReLU2d'

    @classmethod
    def from_float(cls, mod):
        # TODO: Add qat support for BNReLU2d
        return super(BNReLU2d, cls).from_float(mod)

    @classmethod
    def from_reference(cls, bn_relu, output_scale, output_zero_point):
        return super().from_reference(bn_relu[0], output_scale, output_zero_point)

class BNReLU3d(nnq.BatchNorm3d):
    r"""
    A BNReLU3d module is a fused module of BatchNorm3d and ReLU

    We adopt the same interface as :class:`torch.nn.quantized.BatchNorm3d`.

    Attributes:
        Same as torch.nn.quantized.BatchNorm3d

    """
    _FLOAT_MODULE = torch.nn.intrinsic.BNReLU3d

    def __init__(self, num_features, eps=1e-5, momentum=0.1, device=None, dtype=None):
        super(BNReLU3d, self).__init__(num_features, eps=eps, momentum=momentum, device=device, dtype=dtype)

    def forward(self, input):
        # Temporarily using len(shape) instead of ndim due to JIT issue
        # https://github.com/pytorch/pytorch/issues/23890
        if len(input.shape) != 5:
            raise ValueError("Input shape must be `(N, C, D, H, W)`!")
        return torch.ops.quantized.batch_norm3d_relu(
            input, self.weight, self.bias, self.running_mean,
            self.running_var, self.eps, self.scale, self.zero_point)

    def _get_name(self):
        return 'QuantizedBNReLU3d'

    @classmethod
    def from_float(cls, mod):
        # TODO: Add qat support for BNReLU3d
        return super(BNReLU3d, cls).from_float(mod)

    @classmethod
    def from_reference(cls, bn_relu, output_scale, output_zero_point):
        return super().from_reference(bn_relu[0], output_scale, output_zero_point)
