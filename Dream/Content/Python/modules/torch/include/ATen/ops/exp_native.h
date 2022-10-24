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
#include <ATen/ops/exp_meta.h>

namespace at {
namespace native {

struct TORCH_API structured_exp_out : public at::meta::structured_exp {
void impl(const at::Tensor & self, const at::Tensor & out);
};

} // namespace native
} // namespace at
