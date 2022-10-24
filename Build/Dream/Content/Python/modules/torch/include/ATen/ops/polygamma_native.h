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
#include <ATen/ops/polygamma_meta.h>

namespace at {
namespace native {

struct TORCH_API structured_polygamma_out : public at::meta::structured_polygamma {
void impl(int64_t n, const at::Tensor & self, const at::Tensor & out);
};
TORCH_API at::Tensor & polygamma_(at::Tensor & self, int64_t n);

} // namespace native
} // namespace at