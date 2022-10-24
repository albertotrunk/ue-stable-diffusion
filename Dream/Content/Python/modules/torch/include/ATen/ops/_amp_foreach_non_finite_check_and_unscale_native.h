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

TORCH_API ::std::tuple<::std::vector<at::Tensor>,at::Tensor> _amp_foreach_non_finite_check_and_unscale_functional(at::TensorList self, const at::Tensor & found_inf, const at::Tensor & inv_scale);
TORCH_API void _amp_foreach_non_finite_check_and_unscale_cuda_(at::TensorList self, at::Tensor & found_inf, const at::Tensor & inv_scale);

} // namespace native
} // namespace at
