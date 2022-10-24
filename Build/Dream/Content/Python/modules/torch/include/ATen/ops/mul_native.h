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
#include <ATen/ops/mul_meta.h>

namespace at {
namespace native {

struct TORCH_API structured_mul_out : public at::meta::structured_mul_Tensor {
void impl(const at::Tensor & self, const at::Tensor & other, const at::Tensor & out);
};
TORCH_API at::Tensor mul_sparse(const at::Tensor & self, const at::Tensor & other);
TORCH_API at::Tensor & mul_out_sparse_cpu(const at::Tensor & self, const at::Tensor & other, at::Tensor & out);
TORCH_API at::Tensor & mul_sparse_(at::Tensor & self, const at::Tensor & other);
TORCH_API at::Tensor & mul_out_sparse_cuda(const at::Tensor & self, const at::Tensor & other, at::Tensor & out);
TORCH_API at::Tensor mul_sparse_csr(const at::Tensor & self, const at::Tensor & other);
TORCH_API at::Tensor & mul_out_sparse_csr(const at::Tensor & self, const at::Tensor & other, at::Tensor & out);
TORCH_API at::Tensor & mul_sparse_csr_(at::Tensor & self, const at::Tensor & other);
TORCH_API at::Tensor mkldnn_mul(const at::Tensor & self, const at::Tensor & other);
TORCH_API at::Tensor & mkldnn_mul_out(const at::Tensor & self, const at::Tensor & other, at::Tensor & out);
TORCH_API at::Tensor & mkldnn_mul_(at::Tensor & self, const at::Tensor & other);
TORCH_API at::Tensor mul_zerotensor(const at::Tensor & self, const at::Tensor & other);
TORCH_API at::Tensor NestedTensor_mul_Tensor(const at::Tensor & self, const at::Tensor & other);
TORCH_API at::Tensor & NestedTensor_mul__Tensor(at::Tensor & self, const at::Tensor & other);
TORCH_API at::Tensor mul(const at::Tensor & self, const at::Scalar & other);
TORCH_API at::Tensor & mul_(at::Tensor & self, const at::Scalar & other);
TORCH_API at::Tensor mul_scalar_sparse_csr(const at::Tensor & self, const at::Scalar & other);
TORCH_API at::Tensor & mul__scalar_sparse_csr(at::Tensor & self, const at::Scalar & other);

} // namespace native
} // namespace at
