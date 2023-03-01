# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from torchmetrics.classification.confusion_matrix import (  # isort:skip
    BinaryConfusionMatrix,
    ConfusionMatrix,
    MulticlassConfusionMatrix,
    MultilabelConfusionMatrix,
)
from torchmetrics.classification.precision_recall_curve import (  # isort:skip
    PrecisionRecallCurve,
    BinaryPrecisionRecallCurve,
    MulticlassPrecisionRecallCurve,
    MultilabelPrecisionRecallCurve,
)
from torchmetrics.classification.stat_scores import (  # isort:skip
    BinaryStatScores,
    MulticlassStatScores,
    MultilabelStatScores,
    StatScores,
)
from torchmetrics.classification.accuracy import Accuracy, BinaryAccuracy, MulticlassAccuracy, MultilabelAccuracy
from torchmetrics.classification.auroc import AUROC, BinaryAUROC, MulticlassAUROC, MultilabelAUROC
from torchmetrics.classification.average_precision import (
    AveragePrecision,
    BinaryAveragePrecision,
    MulticlassAveragePrecision,
    MultilabelAveragePrecision,
)
from torchmetrics.classification.calibration_error import (
    BinaryCalibrationError,
    CalibrationError,
    MulticlassCalibrationError,
)
from torchmetrics.classification.cohen_kappa import BinaryCohenKappa, CohenKappa, MulticlassCohenKappa
from torchmetrics.classification.dice import Dice
from torchmetrics.classification.exact_match import ExactMatch, MulticlassExactMatch, MultilabelExactMatch
from torchmetrics.classification.f_beta import (
    BinaryF1Score,
    BinaryFBetaScore,
    F1Score,
    FBetaScore,
    MulticlassF1Score,
    MulticlassFBetaScore,
    MultilabelF1Score,
    MultilabelFBetaScore,
)
from torchmetrics.classification.hamming import (
    BinaryHammingDistance,
    HammingDistance,
    MulticlassHammingDistance,
    MultilabelHammingDistance,
)
from torchmetrics.classification.hinge import BinaryHingeLoss, HingeLoss, MulticlassHingeLoss
from torchmetrics.classification.jaccard import (
    BinaryJaccardIndex,
    JaccardIndex,
    MulticlassJaccardIndex,
    MultilabelJaccardIndex,
)
from torchmetrics.classification.matthews_corrcoef import (
    BinaryMatthewsCorrCoef,
    MatthewsCorrCoef,
    MulticlassMatthewsCorrCoef,
    MultilabelMatthewsCorrCoef,
)
from torchmetrics.classification.precision_recall import (
    BinaryPrecision,
    BinaryRecall,
    MulticlassPrecision,
    MulticlassRecall,
    MultilabelPrecision,
    MultilabelRecall,
    Precision,
    Recall,
)
from torchmetrics.classification.ranking import (
    MultilabelCoverageError,
    MultilabelRankingAveragePrecision,
    MultilabelRankingLoss,
)
from torchmetrics.classification.recall_at_fixed_precision import (
    BinaryRecallAtFixedPrecision,
    MulticlassRecallAtFixedPrecision,
    MultilabelRecallAtFixedPrecision,
)
from torchmetrics.classification.roc import ROC, BinaryROC, MulticlassROC, MultilabelROC
from torchmetrics.classification.specificity import (
    BinarySpecificity,
    MulticlassSpecificity,
    MultilabelSpecificity,
    Specificity,
)

__all__ = [
    "BinaryConfusionMatrix",
    "ConfusionMatrix",
    "MulticlassConfusionMatrix",
    "MultilabelConfusionMatrix",
    "PrecisionRecallCurve",
    "BinaryPrecisionRecallCurve",
    "MulticlassPrecisionRecallCurve",
    "MultilabelPrecisionRecallCurve",
    "BinaryStatScores",
    "MulticlassStatScores",
    "MultilabelStatScores",
    "StatScores",
    "Accuracy",
    "BinaryAccuracy",
    "MulticlassAccuracy",
    "MultilabelAccuracy",
    "AUROC",
    "BinaryAUROC",
    "MulticlassAUROC",
    "MultilabelAUROC",
    "AveragePrecision",
    "BinaryAveragePrecision",
    "MulticlassAveragePrecision",
    "MultilabelAveragePrecision",
    "BinnedAveragePrecision",
    "BinnedPrecisionRecallCurve",
    "BinnedRecallAtFixedPrecision",
    "BinaryCalibrationError",
    "CalibrationError",
    "MulticlassCalibrationError",
    "BinaryCohenKappa",
    "CohenKappa",
    "MulticlassCohenKappa",
    "Dice",
    "ExactMatch",
    "MulticlassExactMatch",
    "MultilabelExactMatch",
    "BinaryF1Score",
    "BinaryFBetaScore",
    "F1Score",
    "FBetaScore",
    "MulticlassF1Score",
    "MulticlassFBetaScore",
    "MultilabelF1Score",
    "MultilabelFBetaScore",
    "BinaryHammingDistance",
    "HammingDistance",
    "MulticlassHammingDistance",
    "MultilabelHammingDistance",
    "BinaryHingeLoss",
    "HingeLoss",
    "MulticlassHingeLoss",
    "BinaryJaccardIndex",
    "JaccardIndex",
    "MulticlassJaccardIndex",
    "MultilabelJaccardIndex",
    "BinaryMatthewsCorrCoef",
    "MatthewsCorrCoef",
    "MulticlassMatthewsCorrCoef",
    "MultilabelMatthewsCorrCoef",
    "BinaryPrecision",
    "BinaryRecall",
    "MulticlassPrecision",
    "MulticlassRecall",
    "MultilabelPrecision",
    "MultilabelRecall",
    "Precision",
    "Recall",
    "CoverageError",
    "LabelRankingAveragePrecision",
    "LabelRankingLoss",
    "MultilabelCoverageError",
    "MultilabelRankingAveragePrecision",
    "MultilabelRankingLoss",
    "BinaryRecallAtFixedPrecision",
    "MulticlassRecallAtFixedPrecision",
    "MultilabelRecallAtFixedPrecision",
    "ROC",
    "BinaryROC",
    "MulticlassROC",
    "MultilabelROC",
    "BinarySpecificity",
    "MulticlassSpecificity",
    "MultilabelSpecificity",
    "Specificity",
]
