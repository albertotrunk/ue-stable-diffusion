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



#include <ATen/ops/vdot_ops.h>

namespace at {


// aten::vdot(Tensor self, Tensor other) -> Tensor
TORCH_API inline at::Tensor vdot(const at::Tensor & self, const at::Tensor & other) {
    return at::_ops::vdot::call(self, other);
}

// aten::vdot.out(Tensor self, Tensor other, *, Tensor(a!) out) -> Tensor(a!)
TORCH_API inline at::Tensor & vdot_out(at::Tensor & out, const at::Tensor & self, const at::Tensor & other) {
    return at::_ops::vdot_out::call(self, other, out);
}

// aten::vdot.out(Tensor self, Tensor other, *, Tensor(a!) out) -> Tensor(a!)
TORCH_API inline at::Tensor & vdot_outf(const at::Tensor & self, const at::Tensor & other, at::Tensor & out) {
    return at::_ops::vdot_out::call(self, other, out);
}

}
