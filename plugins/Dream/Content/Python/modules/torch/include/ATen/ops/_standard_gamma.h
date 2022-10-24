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



#include <ATen/ops/_standard_gamma_ops.h>

namespace at {


// aten::_standard_gamma(Tensor self, Generator? generator=None) -> Tensor
TORCH_API inline at::Tensor _standard_gamma(const at::Tensor & self, c10::optional<at::Generator> generator=c10::nullopt) {
    return at::_ops::_standard_gamma::call(self, generator);
}

}