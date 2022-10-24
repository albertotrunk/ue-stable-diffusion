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



#include <ATen/ops/masked_scatter_ops.h>

namespace at {


// aten::masked_scatter(Tensor self, Tensor mask, Tensor source) -> Tensor
TORCH_API inline at::Tensor masked_scatter(const at::Tensor & self, const at::Tensor & mask, const at::Tensor & source) {
    return at::_ops::masked_scatter::call(self, mask, source);
}

// aten::masked_scatter.out(Tensor self, Tensor mask, Tensor source, *, Tensor(a!) out) -> Tensor(a!)
TORCH_API inline at::Tensor & masked_scatter_out(at::Tensor & out, const at::Tensor & self, const at::Tensor & mask, const at::Tensor & source) {
    return at::_ops::masked_scatter_out::call(self, mask, source, out);
}

// aten::masked_scatter.out(Tensor self, Tensor mask, Tensor source, *, Tensor(a!) out) -> Tensor(a!)
TORCH_API inline at::Tensor & masked_scatter_outf(const at::Tensor & self, const at::Tensor & mask, const at::Tensor & source, at::Tensor & out) {
    return at::_ops::masked_scatter_out::call(self, mask, source, out);
}

}
