from typing import Type, Any, Dict, List

from core.executable_level_1.schema import Input, Output
from core.predictor_level_2.predictor import Predictor
from core.executable_level_1.schema import Config

class TransformersModelConfig(Config):    
    def __init__(self, model: Any):
        self.model = model


    def __setattr__(self, name: str, value: Any) -> None: # disable pydantic
        self.__dict__[name] = value


class TransformersModelInput(Input):
    inputs: Any


class TransformersModelOutput(Output):
    outputs: Any


class TransformersModel(
    Predictor[
        TransformersModelConfig, 
        TransformersModelInput, 
        TransformersModelOutput
    ]
):
    input_class: Type[TransformersModelInput] = TransformersModelInput
    output_class: Type[TransformersModelOutput] = TransformersModelOutput
    
    def __init__(self, cfg: TransformersModelConfig) -> None:
        self.cfg = cfg
        super().__init__(cfg)


    def get_predictions(self, inputs: Any) -> Any:
        return self.cfg.model(**inputs) # type: ignore
    

    def invoke(
        self, input_data: TransformersModelInput
    ) -> Dict[str, Any]:
        return {
            'outputs': self.get_predictions(input_data.inputs)
        }
    

    def invoke_batch(
        self, input_data: List[TransformersModelInput]
    ) -> List[Dict[str, Any]]:
        return [self.invoke(i) for i in input_data]