#pragma once

// @generated by torchgen/gen.py from Function.h

#include <ATen/Context.h>
#include <ATen/DeviceGuard.h>
#include <ATen/TensorUtils.h>
#include <ATen/TracerMode.h>
#include <ATen/core/Generator.h>
#include <ATen/core/Reduction.h>
#include <ATen/core/Tensor.h>
#include <c10/core/Scalar.h>
#include <c10/core/Storage.h>
#include <c10/core/TensorOptions.h>
#include <c10/util/Deprecated.h>
#include <c10/util/Optional.h>



#include <ATen/ops/leaky_relu_ops.h>

namespace at {


// aten::leaky_relu.out(Tensor self, Scalar negative_slope=0.01, *, Tensor(a!) out) -> Tensor(a!)
TORCH_API inline at::Tensor & leaky_relu_out(at::Tensor & out, const at::Tensor & self, const at::Scalar & negative_slope=0.01) {
    return at::_ops::leaky_relu_out::call(self, negative_slope, out);
}

// aten::leaky_relu.out(Tensor self, Scalar negative_slope=0.01, *, Tensor(a!) out) -> Tensor(a!)
TORCH_API inline at::Tensor & leaky_relu_outf(const at::Tensor & self, const at::Scalar & negative_slope, at::Tensor & out) {
    return at::_ops::leaky_relu_out::call(self, negative_slope, out);
}

// aten::leaky_relu(Tensor self, Scalar negative_slope=0.01) -> Tensor
TORCH_API inline at::Tensor leaky_relu(const at::Tensor & self, const at::Scalar & negative_slope=0.01) {
    return at::_ops::leaky_relu::call(self, negative_slope);
}

// aten::leaky_relu_(Tensor(a!) self, Scalar negative_slope=0.01) -> Tensor(a!)
TORCH_API inline at::Tensor & leaky_relu_(at::Tensor & self, const at::Scalar & negative_slope=0.01) {
    return at::_ops::leaky_relu_::call(self, negative_slope);
}

}
