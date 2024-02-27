from typing import Type, Any

from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import (
    PredictorInput, PredictorOutput
)
from core.executable_level_1.schema import Config

class TransformersModelConfig(Config):    
    def __init__(self, model: Any):
        self.model = model


    def __setattr__(self, name: str, value: Any) -> None: # disable pydantic
        self.__dict__[name] = value


class TransformersModelInput(PredictorInput):
    ...


class TransformersModelOutput(PredictorOutput):
    ...


class TransformersModel(
    Predictor[
        TransformersModelConfig, 
        TransformersModelInput, 
        TransformersModelOutput
    ]
):
   
    def __init__(
        self, 
        cfg: TransformersModelConfig,
        input_class: Type[TransformersModelInput]=TransformersModelInput,
        output_class: Type[TransformersModelOutput]=TransformersModelOutput
    ) -> None:
        self.cfg = cfg
        super().__init__(cfg, input_class, output_class)


    def get_predictions(self, inputs: Any) -> Any:
        return self.cfg.model(**inputs) # type: ignore