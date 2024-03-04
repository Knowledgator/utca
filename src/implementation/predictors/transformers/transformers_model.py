from typing import TypeVar, Any, Type

from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import (
    PredictorConfig, 
    PredictorInput, 
    PredictorOutput,
    PredictorInputType, 
    PredictorOutputType
)

class TransformersModelConfig(PredictorConfig):    
    def __init__(self, model: Any, **kwargs: Any):
        self.model = model
        self.kwargs = kwargs


    def __setattr__(self, name: str, value: Any) -> None: # disable pydantic
        self.__dict__[name] = value


TransformersModelConfigType = TypeVar(
    'TransformersModelConfigType', 
    bound=TransformersModelConfig, 
)

class TransformersModel(
    Predictor[
        TransformersModelConfigType, 
        PredictorInputType, 
        PredictorOutputType
    ]
):
   
    def __init__(
        self, 
        cfg: TransformersModelConfigType,
        input_class: Type[PredictorInputType]=PredictorInput,
        output_class: Type[PredictorOutputType]=PredictorOutput
    ) -> None:
        self.cfg = cfg
        super().__init__(cfg, input_class, output_class)


    def get_predictions(self, **inputs: Any) -> Any:
        if not "encodings" in inputs:
            return self.cfg.model(**inputs, **self.cfg.kwargs)
        else:
            return self.cfg.model(**inputs["encodings"], **self.cfg.kwargs)
    

class TransformersGenerativeModel(
    TransformersModel[
        TransformersModelConfigType, 
        PredictorInputType, 
        PredictorOutputType
    ]
):
    def get_predictions(self, **inputs: Any) -> Any:
        return self.cfg.model.generate(**inputs, **self.cfg.kwargs) # type: ignore