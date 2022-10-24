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



#include <ATen/ops/_unique_ops.h>

namespace at {


// aten::_unique(Tensor self, bool sorted=True, bool return_inverse=False) -> (Tensor, Tensor)
TORCH_API inline ::std::tuple<at::Tensor,at::Tensor> _unique(const at::Tensor & self, bool sorted=true, bool return_inverse=false) {
    return at::_ops::_unique::call(self, sorted, return_inverse);
}

}