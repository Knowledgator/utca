from typing import Any
from abc import abstractmethod

from core.executable_level_1.executable import Executable
from core.predictor_level_2.schema import (
    PredictorInputType,
    PredictorOutputType,
    PredictorConfigType
)

class Predictor(Executable[PredictorConfigType, PredictorInputType, PredictorOutputType]):
    @abstractmethod
    def get_predictions(self, inputs: Any) -> Any:
        ...