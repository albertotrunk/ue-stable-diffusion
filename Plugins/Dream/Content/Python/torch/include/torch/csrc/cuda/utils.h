#ifndef THCP_UTILS_H
#define THCP_UTILS_H

#define THCPUtils_(NAME) TH_CONCAT_4(THCP,Real,Utils_,NAME)

#define THCTensorPtr   TH_CONCAT_3(THC,Real,TensorPtr)
#define THCPStoragePtr TH_CONCAT_3(THCP,Real,StoragePtr)
#define THCPTensorPtr  TH_CONCAT_3(THCP,Real,TensorPtr)

#define THCSTensorPtr  TH_CONCAT_3(THCS,Real,TensorPtr)
#define THCSPTensorPtr TH_CONCAT_3(THCSP,Real,TensorPtr)

#include <torch/csrc/cuda/override_macros.h>

#define THC_GENERIC_FILE "torch/csrc/generic/utils.h"
#include <torch/csrc/THCGenerateByteType.h>
#endif
