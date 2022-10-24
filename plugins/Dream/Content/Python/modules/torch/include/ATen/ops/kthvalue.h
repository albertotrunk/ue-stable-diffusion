#pragma once

// @generated by torchgen/gen.py from Function.h

#include <ATen/Context.h>
#include <ATen/DeviceGuard.h>
#include <ATen/TensorUtils.h>
#include <ATen/TracerMode.h>
#include <ATen/core/Generator.h>
#include <ATen/core/Reduction.h>
#include <ATen/core/Tensor.h>
#include <c10/core/Scalar.h>
#include <c10/core/Storage.h>
#include <c10/core/TensorOptions.h>
#include <c10/util/Deprecated.h>
#include <c10/util/Optional.h>



#include <ATen/ops/kthvalue_ops.h>

namespace at {


// aten::kthvalue(Tensor self, int k, int dim=-1, bool keepdim=False) -> (Tensor values, Tensor indices)
TORCH_API inline ::std::tuple<at::Tensor,at::Tensor> kthvalue(const at::Tensor & self, int64_t k, int64_t dim=-1, bool keepdim=false) {
    return at::_ops::kthvalue::call(self, k, dim, keepdim);
}

// aten::kthvalue.values(Tensor self, int k, int dim=-1, bool keepdim=False, *, Tensor(a!) values, Tensor(b!) indices) -> (Tensor(a!) values, Tensor(b!) indices)
TORCH_API inline ::std::tuple<at::Tensor &,at::Tensor &> kthvalue_out(at::Tensor & values, at::Tensor & indices, const at::Tensor & self, int64_t k, int64_t dim=-1, bool keepdim=false) {
    return at::_ops::kthvalue_values::call(self, k, dim, keepdim, values, indices);
}

// aten::kthvalue.values(Tensor self, int k, int dim=-1, bool keepdim=False, *, Tensor(a!) values, Tensor(b!) indices) -> (Tensor(a!) values, Tensor(b!) indices)
TORCH_API inline ::std::tuple<at::Tensor &,at::Tensor &> kthvalue_outf(const at::Tensor & self, int64_t k, int64_t dim, bool keepdim, at::Tensor & values, at::Tensor & indices) {
    return at::_ops::kthvalue_values::call(self, k, dim, keepdim, values, indices);
}

// aten::kthvalue.dimname(Tensor self, int k, Dimname dim, bool keepdim=False) -> (Tensor values, Tensor indices)
TORCH_API inline ::std::tuple<at::Tensor,at::Tensor> kthvalue(const at::Tensor & self, int64_t k, at::Dimname dim, bool keepdim=false) {
    return at::_ops::kthvalue_dimname::call(self, k, dim, keepdim);
}

// aten::kthvalue.dimname_out(Tensor self, int k, Dimname dim, bool keepdim=False, *, Tensor(a!) values, Tensor(b!) indices) -> (Tensor(a!) values, Tensor(b!) indices)
TORCH_API inline ::std::tuple<at::Tensor &,at::Tensor &> kthvalue_out(at::Tensor & values, at::Tensor & indices, const at::Tensor & self, int64_t k, at::Dimname dim, bool keepdim=false) {
    return at::_ops::kthvalue_dimname_out::call(self, k, dim, keepdim, values, indices);
}

// aten::kthvalue.dimname_out(Tensor self, int k, Dimname dim, bool keepdim=False, *, Tensor(a!) values, Tensor(b!) indices) -> (Tensor(a!) values, Tensor(b!) indices)
TORCH_API inline ::std::tuple<at::Tensor &,at::Tensor &> kthvalue_outf(const at::Tensor & self, int64_t k, at::Dimname dim, bool keepdim, at::Tensor & values, at::Tensor & indices) {
    return at::_ops::kthvalue_dimname_out::call(self, k, dim, keepdim, values, indices);
}

}
