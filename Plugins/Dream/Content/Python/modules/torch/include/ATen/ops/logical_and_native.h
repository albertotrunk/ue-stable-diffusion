#pragma once

// @generated by torchgen/gen.py from NativeFunction.h

#include <c10/core/Scalar.h>
#include <c10/core/Storage.h>
#include <c10/core/TensorOptions.h>
#include <c10/util/Deprecated.h>
#include <c10/util/Optional.h>
#include <c10/core/QScheme.h>
#include <ATen/core/Reduction.h>
#include <ATen/core/Tensor.h>
#include <tuple>
#include <vector>


namespace at {
namespace native {

TORCH_API at::Tensor logical_and(const at::Tensor & self, const at::Tensor & other);
TORCH_API at::Tensor & logical_and_(at::Tensor & self, const at::Tensor & other);
TORCH_API at::Tensor & logical_and_out(const at::Tensor & self, const at::Tensor & other, at::Tensor & out);

} // namespace native
} // namespace at
