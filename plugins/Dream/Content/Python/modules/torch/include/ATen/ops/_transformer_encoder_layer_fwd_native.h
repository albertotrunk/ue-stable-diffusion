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

TORCH_API at::Tensor transformer_encoder_layer_forward(const at::Tensor & src, int64_t embed_dim, int64_t num_heads, const at::Tensor & qkv_weight, const at::Tensor & qkv_bias, const at::Tensor & proj_weight, const at::Tensor & proj_bias, bool use_gelu, bool norm_first, double eps, const at::Tensor & norm_weight_1, const at::Tensor & norm_bias_1, const at::Tensor & norm_weight_2, const at::Tensor & norm_bias_2, const at::Tensor & ffn_weight_1, const at::Tensor & ffn_bias_1, const at::Tensor & ffn_weight_2, const at::Tensor & ffn_bias_2, const c10::optional<at::Tensor> & mask={});

} // namespace native
} // namespace at
