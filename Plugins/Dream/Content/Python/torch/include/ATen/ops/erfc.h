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



#include <ATen/ops/erfc_ops.h>

namespace at {


// aten::erfc(Tensor self) -> Tensor
TORCH_API inline at::Tensor erfc(const at::Tensor & self) {
    return at::_ops::erfc::call(self);
}

// aten::erfc_(Tensor(a!) self) -> Tensor(a!)
TORCH_API inline at::Tensor & erfc_(at::Tensor & self) {
    return at::_ops::erfc_::call(self);
}

// aten::erfc.out(Tensor self, *, Tensor(a!) out) -> Tensor(a!)
TORCH_API inline at::Tensor & erfc_out(at::Tensor & out, const at::Tensor & self) {
    return at::_ops::erfc_out::call(self, out);
}

// aten::erfc.out(Tensor self, *, Tensor(a!) out) -> Tensor(a!)
TORCH_API inline at::Tensor & erfc_outf(const at::Tensor & self, at::Tensor & out) {
    return at::_ops::erfc_out::call(self, out);
}

}
