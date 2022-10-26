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



#include <ATen/ops/_foreach_zero_ops.h>

namespace at {


// aten::_foreach_zero_(Tensor(a!)[] self) -> ()
TORCH_API inline void _foreach_zero_(at::TensorList self) {
    return at::_ops::_foreach_zero_::call(self);
}

// aten::_foreach_zero.out(Tensor[] self, *, Tensor(a!)[] out) -> ()
TORCH_API inline void _foreach_zero_out(at::TensorList out, at::TensorList self) {
    return at::_ops::_foreach_zero_out::call(self, out);
}

// aten::_foreach_zero.out(Tensor[] self, *, Tensor(a!)[] out) -> ()
TORCH_API inline void _foreach_zero_outf(at::TensorList self, at::TensorList out) {
    return at::_ops::_foreach_zero_out::call(self, out);
}

// aten::_foreach_zero.functional(Tensor[] self) -> Tensor[] self_out
TORCH_API inline ::std::vector<at::Tensor> _foreach_zero_functional(at::TensorList self) {
    return at::_ops::_foreach_zero_functional::call(self);
}

}