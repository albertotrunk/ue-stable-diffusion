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



#include <ATen/ops/hstack_ops.h>

namespace at {


// aten::hstack(Tensor[] tensors) -> Tensor
TORCH_API inline at::Tensor hstack(at::TensorList tensors) {
    return at::_ops::hstack::call(tensors);
}

// aten::hstack.out(Tensor[] tensors, *, Tensor(a!) out) -> Tensor(a!)
TORCH_API inline at::Tensor & hstack_out(at::Tensor & out, at::TensorList tensors) {
    return at::_ops::hstack_out::call(tensors, out);
}

// aten::hstack.out(Tensor[] tensors, *, Tensor(a!) out) -> Tensor(a!)
TORCH_API inline at::Tensor & hstack_outf(at::TensorList tensors, at::Tensor & out) {
    return at::_ops::hstack_out::call(tensors, out);
}

}
