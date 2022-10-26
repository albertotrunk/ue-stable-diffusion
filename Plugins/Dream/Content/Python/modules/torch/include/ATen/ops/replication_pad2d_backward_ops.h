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


struct TORCH_API replication_pad2d_backward_grad_input {
  using schema = at::Tensor & (const at::Tensor &, const at::Tensor &, at::IntArrayRef, at::Tensor &);
  using ptr_schema = schema*;
  // See Note [static constexpr char* members for windows NVCC]
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(name, "aten::replication_pad2d_backward")
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(overload_name, "grad_input")
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(schema_str, "replication_pad2d_backward.grad_input(Tensor grad_output, Tensor self, int[4] padding, *, Tensor(a!) grad_input) -> Tensor(a!)")
  static at::Tensor & call(const at::Tensor & grad_output, const at::Tensor & self, at::IntArrayRef padding, at::Tensor & grad_input);
  static at::Tensor & redispatch(c10::DispatchKeySet dispatchKeySet, const at::Tensor & grad_output, const at::Tensor & self, at::IntArrayRef padding, at::Tensor & grad_input);
};

struct TORCH_API replication_pad2d_backward {
  using schema = at::Tensor (const at::Tensor &, const at::Tensor &, at::IntArrayRef);
  using ptr_schema = schema*;
  // See Note [static constexpr char* members for windows NVCC]
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(name, "aten::replication_pad2d_backward")
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(overload_name, "")
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(schema_str, "replication_pad2d_backward(Tensor grad_output, Tensor self, int[4] padding) -> Tensor")
  static at::Tensor call(const at::Tensor & grad_output, const at::Tensor & self, at::IntArrayRef padding);
  static at::Tensor redispatch(c10::DispatchKeySet dispatchKeySet, const at::Tensor & grad_output, const at::Tensor & self, at::IntArrayRef padding);
};

}} // namespace at::_ops
