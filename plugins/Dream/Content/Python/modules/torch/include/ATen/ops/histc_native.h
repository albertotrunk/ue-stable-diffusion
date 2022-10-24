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

TORCH_API at::Tensor histogram_histc_cpu(const at::Tensor & self, int64_t bins=100, const at::Scalar & min=0, const at::Scalar & max=0);
TORCH_API at::Tensor & histogram_histc_cpu_out(const at::Tensor & self, int64_t bins, const at::Scalar & min, const at::Scalar & max, at::Tensor & out);
TORCH_API at::Tensor _histc_cuda(const at::Tensor & self, int64_t bins=100, const at::Scalar & min=0, const at::Scalar & max=0);
TORCH_API at::Tensor & _histc_out_cuda(const at::Tensor & self, int64_t bins, const at::Scalar & min, const at::Scalar & max, at::Tensor & out);

} // namespace native
} // namespace at
