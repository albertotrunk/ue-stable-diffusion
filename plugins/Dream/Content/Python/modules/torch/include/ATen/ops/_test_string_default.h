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



#include <ATen/ops/_test_string_default_ops.h>

namespace at {


// aten::_test_string_default(Tensor dummy, str a="\"'\\", str b='"\'\\') -> Tensor
TORCH_API inline at::Tensor _test_string_default(const at::Tensor & dummy, c10::string_view a="\"'\\", c10::string_view b="\"'\\") {
    return at::_ops::_test_string_default::call(dummy, a, b);
}

}