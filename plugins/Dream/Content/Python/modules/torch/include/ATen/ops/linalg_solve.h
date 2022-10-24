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



#include <ATen/ops/linalg_solve_ops.h>

namespace at {


// aten::linalg_solve(Tensor input, Tensor other) -> Tensor
TORCH_API inline at::Tensor linalg_solve(const at::Tensor & input, const at::Tensor & other) {
    return at::_ops::linalg_solve::call(input, other);
}

// aten::linalg_solve.out(Tensor input, Tensor other, *, Tensor(a!) out) -> Tensor(a!)
TORCH_API inline at::Tensor & linalg_solve_out(at::Tensor & out, const at::Tensor & input, const at::Tensor & other) {
    return at::_ops::linalg_solve_out::call(input, other, out);
}

// aten::linalg_solve.out(Tensor input, Tensor other, *, Tensor(a!) out) -> Tensor(a!)
TORCH_API inline at::Tensor & linalg_solve_outf(const at::Tensor & input, const at::Tensor & other, at::Tensor & out) {
    return at::_ops::linalg_solve_out::call(input, other, out);
}

}
