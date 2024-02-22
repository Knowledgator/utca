from typing import Type, Any, Dict, List

from PIL import Image

from core.executable_level_1.schema import Input, Output
from core.predictor_level_2.predictor import Predictor
from core.executable_level_1.schema import Config

class TransformersImageClassificationConfig(Config):    
    def __init__(self, model: Any, feature_extractor: Any):
        self.model = model
        self.feature_extractor = feature_extractor


    def __setattr__(self, name: str, value: Any) -> None: # disable pydantic
        self.__dict__[name] = value


class TransformersImageClassificationInput(Input):
    def __init__(self, image: Image.Image):
        self.image: Image.Image = image


    def __setattr__(self, name: str, value: Any) -> None: # disable pydantic
        self.__dict__[name] = value


class TransformersImageClassificationOutput(Output):
    outputs: Any


class TransformersImageClassification(
    Predictor[
        TransformersImageClassificationConfig, 
        TransformersImageClassificationInput, 
        TransformersImageClassificationOutput
    ]
):
    input_class: Type[TransformersImageClassificationInput] = TransformersImageClassificationInput
    output_class: Type[TransformersImageClassificationOutput] = TransformersImageClassificationOutput
    
    def __init__(self, cfg: TransformersImageClassificationConfig) -> None:
        self.cfg = cfg
        super().__init__(cfg)


    def get_predictions(self, inputs: Any) -> Any:
        inputs = self.cfg.feature_extractor(images=inputs, return_tensors="pt")
        return self.cfg.model(**inputs) # type: ignore
    

    def invoke(
        self, input_data: TransformersImageClassificationInput
    ) -> Dict[str, Any]:
        return {
            'outputs': self.get_predictions(input_data.image)
        }
    

    def invoke_batch(
        self, input_data: List[TransformersImageClassificationInput]
    ) -> List[Dict[str, Any]]:
        return [self.invoke(i) for i in input_data]