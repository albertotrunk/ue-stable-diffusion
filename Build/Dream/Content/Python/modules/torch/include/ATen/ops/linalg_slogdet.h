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



#include <ATen/ops/linalg_slogdet_ops.h>

namespace at {


// aten::linalg_slogdet(Tensor self) -> (Tensor sign, Tensor logabsdet)
TORCH_API inline ::std::tuple<at::Tensor,at::Tensor> linalg_slogdet(const at::Tensor & self) {
    return at::_ops::linalg_slogdet::call(self);
}

// aten::linalg_slogdet.out(Tensor self, *, Tensor(a!) sign, Tensor(b!) logabsdet) -> (Tensor(a!) sign, Tensor(b!) logabsdet)
TORCH_API inline ::std::tuple<at::Tensor &,at::Tensor &> linalg_slogdet_out(at::Tensor & sign, at::Tensor & logabsdet, const at::Tensor & self) {
    return at::_ops::linalg_slogdet_out::call(self, sign, logabsdet);
}

// aten::linalg_slogdet.out(Tensor self, *, Tensor(a!) sign, Tensor(b!) logabsdet) -> (Tensor(a!) sign, Tensor(b!) logabsdet)
TORCH_API inline ::std::tuple<at::Tensor &,at::Tensor &> linalg_slogdet_outf(const at::Tensor & self, at::Tensor & sign, at::Tensor & logabsdet) {
    return at::_ops::linalg_slogdet_out::call(self, sign, logabsdet);
}

}
