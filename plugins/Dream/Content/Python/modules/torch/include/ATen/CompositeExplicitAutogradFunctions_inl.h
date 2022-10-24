#pragma once
// @generated by torchgen/gen.py from DispatchKeyFunctions_inl.h

// NB: The implementing C++ file is RegisterDispatchKey.cpp

// The only #includes we need are for custom classes that have defaults in the C++ API
#include <c10/core/MemoryFormat.h>
#include <c10/core/Scalar.h>
#include <ATen/core/Reduction.h>

#if defined(AT_PER_OPERATOR_HEADERS) && defined(TORCH_ASSERT_ONLY_METHOD_OPERATORS)
#error This change adds a dependency on all pytorch operators, meaning the     \
  file will need to be re-compiled every time an operator is changed or added. \
  Consider including a specific operator from                                  \
  <ATen/ops/{my_operator}_compositeexplicitautograd_dispatch.h>.                   \
  See NOTE [TORCH_ASSERT_ONLY_METHOD_OPERATORS].
#endif

#include <ATen/ops/_addmm_activation_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_amp_foreach_non_finite_check_and_unscale_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_amp_update_scale_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_coalesced_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_conj_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_conj_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_conj_physical_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_convert_indices_from_coo_to_csr_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_convert_indices_from_csr_to_coo_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_convolution_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_euclidean_dist_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_abs_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_acos_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_add_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_addcdiv_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_addcmul_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_asin_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_atan_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_ceil_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_cos_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_cosh_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_div_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_erf_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_erfc_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_exp_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_expm1_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_floor_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_frac_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_lgamma_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_log_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_log10_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_log1p_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_log2_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_mul_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_neg_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_reciprocal_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_round_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_sigmoid_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_sin_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_sinh_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_sqrt_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_sub_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_tan_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_tanh_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_trunc_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_foreach_zero_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_fused_moving_avg_obs_fq_helper_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_fw_primal_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_fw_primal_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_grid_sampler_2d_cpu_fallback_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_has_same_storage_numel_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_index_put_impl_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_indices_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_linalg_check_errors_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_linalg_inv_out_helper_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_linalg_svd_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_log_softmax_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_log_softmax_backward_data_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_make_dual_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_make_dual_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_neg_view_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_neg_view_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_new_zeros_with_same_feature_meta_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_nnpack_spatial_convolution_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_pack_padded_sequence_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_reshape_alias_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_resize_output_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_softmax_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_softmax_backward_data_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_sparse_addmm_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_sparse_broadcast_to_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_sparse_sum_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_stack_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_test_warn_in_autograd_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_to_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_trilinear_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_unsafe_view_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_upsample_bicubic2d_aa_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_upsample_bicubic2d_aa_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_upsample_bilinear2d_aa_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_upsample_bilinear2d_aa_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_upsample_nearest_exact1d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_upsample_nearest_exact1d_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_upsample_nearest_exact2d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_upsample_nearest_exact2d_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_upsample_nearest_exact3d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_upsample_nearest_exact3d_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/_values_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/abs_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/acos_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/acosh_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/adaptive_max_pool2d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/adaptive_max_pool2d_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/adaptive_max_pool3d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/adaptive_max_pool3d_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/add_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/addcdiv_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/addcmul_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/addmm_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/addmv_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/addr_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/affine_grid_generator_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/alias_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/alias_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/all_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/amax_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/amin_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/aminmax_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/any_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/argmax_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/argmin_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/as_strided_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/as_strided_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/asin_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/asinh_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/atan_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/atan2_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/atanh_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/avg_pool2d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/avg_pool2d_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/avg_pool3d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/avg_pool3d_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/baddbmm_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/bernoulli_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/binary_cross_entropy_with_logits_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/bitwise_and_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/bitwise_left_shift_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/bitwise_not_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/bitwise_or_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/bitwise_right_shift_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/bitwise_xor_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/bmm_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/cat_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/cauchy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/ccol_indices_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/ceil_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/celu_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/cholesky_solve_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/clamp_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/clamp_max_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/clamp_min_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/clone_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/col_indices_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/complex_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/conj_physical_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/constant_pad_nd_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/conv_tbc_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/convolution_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/convolution_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/convolution_backward_overrideable_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/convolution_overrideable_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/copy_sparse_to_sparse_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/copysign_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/cos_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/cosh_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/count_nonzero_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/crow_indices_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/cummax_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/cummin_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/cumprod_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/cumsum_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/deg2rad_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/detach_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/detach_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/diag_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/diag_embed_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/diagonal_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/diagonal_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/diagonal_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/diagonal_scatter_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/digamma_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/dist_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/div_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/dot_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/eig_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/elu_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/elu_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/embedding_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/embedding_renorm_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/empty_like_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/eq_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/erf_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/erfc_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/erfinv_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/exp_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/exp2_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/expand_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/expand_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/expm1_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/exponential_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/fill_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/floor_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/fmax_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/fmin_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/fmod_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/frac_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/fractional_max_pool2d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/fractional_max_pool2d_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/fractional_max_pool3d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/frexp_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/gather_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/gcd_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/ge_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/gelu_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/gelu_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/geometric_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/glu_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/gt_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/hardshrink_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/hardshrink_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/hardsigmoid_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/hardsigmoid_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/heaviside_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/huber_loss_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/hypot_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/i0_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/igamma_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/igammac_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/index_add_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/index_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/index_fill_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/index_put_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/index_reduce_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/indices_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/inverse_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/is_pinned_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/isin_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/isinf_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/isneginf_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/isposinf_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/kl_div_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/kthvalue_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/l1_loss_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/l1_loss_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/lcm_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/le_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/leaky_relu_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/leaky_relu_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/lerp_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/lgamma_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/lift_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/linalg_cross_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/linalg_inv_ex_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/linalg_ldl_factor_ex_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/linalg_ldl_solve_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/linalg_lstsq_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/linalg_lu_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/linalg_lu_factor_ex_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/linalg_pinv_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/linalg_qr_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/linalg_vector_norm_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/log_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/log10_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/log1p_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/log2_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/log_normal_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/log_softmax_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/logaddexp_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/logaddexp2_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/logcumsumexp_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/logdet_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/logical_and_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/logical_not_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/logical_or_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/logical_xor_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/logit_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/logsumexp_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/lt_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/lu_unpack_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/masked_fill_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/masked_scatter_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/max_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/max_pool2d_with_indices_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/max_pool2d_with_indices_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/maximum_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/mean_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/median_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/min_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/minimum_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/mish_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/mkldnn_convolution_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/mm_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/mode_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/mse_loss_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/mul_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/mv_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/mvlgamma_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/nan_to_num_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/nanmedian_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/narrow_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/ne_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/neg_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/new_empty_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/new_empty_strided_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/nextafter_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/nll_loss_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/nll_loss_forward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/norm_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/normal_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/permute_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/permute_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/pixel_shuffle_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/pixel_unshuffle_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/polar_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/polygamma_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/pow_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/prod_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/rad2deg_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/random_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/reciprocal_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/reflection_pad1d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/reflection_pad1d_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/reflection_pad3d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/reflection_pad3d_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/remainder_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/renorm_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/repeat_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/replication_pad1d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/replication_pad1d_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/replication_pad2d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/replication_pad3d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/resize_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/resize_as_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/resize_as_sparse_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/rot90_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/round_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/row_indices_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/rrelu_with_noise_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/rsqrt_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/rsub_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/scatter_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/scatter_add_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/scatter_reduce_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/select_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/select_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/select_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/select_scatter_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/set_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/sgn_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/sigmoid_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/sigmoid_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/sign_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/signbit_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/silu_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/silu_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/sin_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/sinc_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/sinh_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/slice_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/slice_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/slice_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/slice_scatter_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/slogdet_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/slow_conv_transpose2d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/smooth_l1_loss_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/smooth_l1_loss_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/soft_margin_loss_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/soft_margin_loss_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/softmax_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/softplus_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/softplus_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/softshrink_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/softshrink_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/sort_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/sparse_resize_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/sparse_resize_and_clear_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/special_entr_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/special_erfcx_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/special_i0e_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/special_i1_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/special_i1e_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/special_log_ndtr_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/special_ndtri_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/special_xlog1py_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/special_zeta_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/split_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/split_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/split_with_sizes_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/split_with_sizes_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/sqrt_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/squeeze_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/squeeze_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/stack_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/sub_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/sum_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/symeig_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/t_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/t_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/tan_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/tanh_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/tanh_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/threshold_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/threshold_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/topk_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/transpose_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/transpose_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/triangular_solve_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/tril_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/triu_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/trunc_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/unbind_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/unbind_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/unfold_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/uniform_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/unsafe_split_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/unsafe_split_with_sizes_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/unsqueeze_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/unsqueeze_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/upsample_bicubic2d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/upsample_bicubic2d_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/upsample_bilinear2d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/upsample_bilinear2d_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/upsample_linear1d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/upsample_linear1d_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/upsample_nearest1d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/upsample_nearest1d_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/upsample_nearest2d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/upsample_nearest2d_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/upsample_nearest3d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/upsample_nearest3d_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/upsample_trilinear3d_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/upsample_trilinear3d_backward_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/values_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/vdot_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/view_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/view_as_complex_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/view_as_real_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/view_copy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/xlogy_compositeexplicitautograd_dispatch.h>
#include <ATen/ops/zero_compositeexplicitautograd_dispatch.h>

namespace at {
namespace compositeexplicitautograd {



} // namespace compositeexplicitautograd
} // namespace at
