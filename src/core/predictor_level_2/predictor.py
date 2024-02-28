from typing import Any, Dict, List
from abc import abstractmethod

from core.executable_level_1.executable import Executable
from core.predictor_level_2.schema import (
    PredictorInputType,
    PredictorOutputType,
    PredictorConfigType
)

class Predictor(
    Executable[
        PredictorConfigType, 
        PredictorInputType, 
        PredictorOutputType
    ]
):
    @abstractmethod
    def get_predictions(self, **inputs: Any) -> Any:
        ...

    
    def invoke(
        self, input_data: PredictorInputType
    ) -> Dict[str, Any]:
        return {
            'outputs': self.get_predictions(**input_data.inputs)
        }
    

    def invoke_batch(
        self, input_data: List[PredictorInputType]
    ) -> List[Dict[str, Any]]:
        return [self.invoke(i) for i in input_data]