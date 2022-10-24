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



#include <ATen/ops/_pdist_forward_ops.h>

namespace at {


// aten::_pdist_forward(Tensor self, float p=2) -> Tensor
TORCH_API inline at::Tensor _pdist_forward(const at::Tensor & self, double p=2) {
    return at::_ops::_pdist_forward::call(self, p);
}

}
