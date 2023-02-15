#pragma once

// @generated by torchgen/gen.py from Operator.h

#include <tuple>
#include <vector>

// Forward declarations of any types needed in the operator signatures.
// We can't directly include these classes because it will cause circular include dependencies.
// This file is included by TensorBody.h, which defines the Tensor class.
#include <ATen/core/ATen_fwd.h>

namespace at {
namespace _ops {


struct TORCH_API index_Tensor {
  using schema = at::Tensor (const at::Tensor &, const c10::List<c10::optional<at::Tensor>> &);
  using ptr_schema = schema*;
  // See Note [static constexpr char* members for windows NVCC]
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(name, "aten::index")
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(overload_name, "Tensor")
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(schema_str, "index.Tensor(Tensor self, Tensor?[] indices) -> Tensor")
  static at::Tensor call(const at::Tensor & self, const c10::List<c10::optional<at::Tensor>> & indices);
  static at::Tensor redispatch(c10::DispatchKeySet dispatchKeySet, const at::Tensor & self, const c10::List<c10::optional<at::Tensor>> & indices);
};

}} // namespace at::_ops
