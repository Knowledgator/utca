from typing import Any, Dict
from abc import abstractmethod

from core.executable_level_1.executable import Executable
from core.predictor_level_2.schema import (
    PredictorInputType,
    PredictorOutputType,
)

class Predictor(
    Executable[
        PredictorInputType, 
        PredictorOutputType
    ]
):

    @abstractmethod
    def invoke(
        self, input_data: PredictorInputType
    ) -> Dict[str, Any]:
        ...
    

    @property
    @abstractmethod
    def config(self) -> Any:
        ...