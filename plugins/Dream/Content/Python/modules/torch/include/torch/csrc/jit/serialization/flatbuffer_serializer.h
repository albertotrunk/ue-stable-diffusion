#pragma once

#include <ATen/core/qualified_name.h>
#include <flatbuffers/flatbuffers.h>
#include <string>
#include <vector>

#include <ATen/core/ivalue.h>
#include <ATen/core/jit_type.h>
#include <torch/csrc/jit/backends/backend_debug_handler.h>
#include <torch/csrc/jit/mobile/module.h>
#include <torch/csrc/jit/serialization/type_name_uniquer.h>

#include <torch/csrc/jit/serialization/mobile_bytecode_generated.h> // NOLINT

namespace torch {
namespace jit {

TORCH_API void save_mobile_module(
    const mobile::Module& module,
    const std::string& filename,
    const ExtraFilesMap& extra_files = ExtraFilesMap(),
    const ExtraFilesMap& jit_sources = ExtraFilesMap(),
    const std::vector<IValue>& jit_constants = {});

TORCH_API flatbuffers::DetachedBuffer save_mobile_module_to_bytes(
    const mobile::Module& module,
    const ExtraFilesMap& extra_files = ExtraFilesMap(),
    const ExtraFilesMap& jit_sources = ExtraFilesMap(),
    const std::vector<IValue>& jit_constants = {});

} // namespace jit
} // namespace torch
