// This file defines classes for registering standard lowerings from JIT to TE
// IR.
#pragma once

#include <c10/util/variant.h>
#include <torch/csrc/jit/ir/ir.h>
#include <torch/csrc/jit/runtime/interpreter.h>
#include <torch/csrc/jit/tensorexpr/analysis.h>
#include <torch/csrc/jit/tensorexpr/codegen.h>
#include <torch/csrc/jit/tensorexpr/tensor.h>

namespace torch {
namespace jit {
namespace tensorexpr {

using ArgNone = c10::monostate;
using BufList = std::vector<tensorexpr::BufHandle>;
using DoubleList = std::vector<double>;
using IntList = std::vector<int64_t>;
using ArgValue = c10::variant<
    tensorexpr::BufHandle,
    tensorexpr::VarHandle,
    double,
    int64_t,
    bool,
    BufList,
    DoubleList,
    IntList,
    std::string,
    ArgNone>;

using NNCLoweringFunction = std::function<Tensor(
    const std::vector<ArgValue>&,
    const std::vector<ExprHandle>&,
    const std::vector<ExprHandle>&,
    const c10::optional<ScalarType>&,
    at::Device)>;

TORCH_API FunctionSchemaMap<NNCLoweringFunction>& getNNCLoweringRegistry();
TORCH_API NNCLoweringFunction getStandardLoweringFor(const std::string& op);

struct RegisterNNCLoweringsFunction {
  RegisterNNCLoweringsFunction(
      const std::vector<std::string>& schemas,
      NNCLoweringFunction fn);
};

} // namespace tensorexpr
} // namespace jit
} // namespace torch
