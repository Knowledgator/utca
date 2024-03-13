from typing import TypeVar, Any, Type, Dict, Optional

from transformers import PreTrainedModel # type: ignore

from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import (
    PredictorConfig, 
    PredictorInput, 
    PredictorOutput,
    PredictorInputType, 
    PredictorOutputType
)

class TransformersModelConfig(PredictorConfig):
    class Config:
        arbitrary_types_allowed = True

    model: PreTrainedModel
    kwargs: Optional[Dict[str, Any]]=None

    def get_kwargs(self) -> Dict[str, Any]:
        return self.kwargs or {}


TransformersModelConfigType = TypeVar(
    'TransformersModelConfigType', 
    bound=TransformersModelConfig, 
)

class TransformersModel(
    Predictor[
        PredictorInputType, 
        PredictorOutputType
    ]
):
   
    def __init__(
        self, 
        cfg: TransformersModelConfig,
        input_class: Type[PredictorInputType]=PredictorInput,
        output_class: Type[PredictorOutputType]=PredictorOutput
    ) -> None:
        self.cfg = cfg
        super().__init__(input_class, output_class)


    def get_predictions(self, **inputs: Any) -> Any:
        if not "encodings" in inputs:
            return self.cfg.model(**inputs, **self.cfg.get_kwargs())
        else:
            return self.cfg.model(**inputs.pop("encodings"), **inputs, **self.cfg.get_kwargs())
    

    @property
    def config(self) -> Any:
        return self.cfg.model.config # type: ignore


class TransformersGenerativeModel(
    TransformersModel[
        PredictorInputType, 
        PredictorOutputType
    ]
):
    def get_predictions(self, **inputs: Any) -> Any:
        if not "encodings" in inputs:
            return self.cfg.model.generate(**inputs, **self.cfg.get_kwargs()) # type: ignore
        else:
            return self.cfg.model.generate(**inputs.pop("encodings"), **inputs, **self.cfg.get_kwargs()) # type: ignore