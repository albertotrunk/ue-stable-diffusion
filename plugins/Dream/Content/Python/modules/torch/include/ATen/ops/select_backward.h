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



#include <ATen/ops/select_backward_ops.h>

namespace at {


// aten::select_backward(Tensor grad_output, int[] input_sizes, int dim, int index) -> Tensor
TORCH_API inline at::Tensor select_backward(const at::Tensor & grad_output, at::IntArrayRef input_sizes, int64_t dim, int64_t index) {
    return at::_ops::select_backward::call(grad_output, input_sizes, dim, index);
}

}
