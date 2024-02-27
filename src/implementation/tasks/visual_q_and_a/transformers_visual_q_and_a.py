from typing import Type, Optional, Any, List, Dict, Union

from PIL import Image

from core.executable_level_1.schema import Config, Input, Output
from core.executable_level_1.actions import (
    Action, InputState, OutputState
)
from core.task_level_3.task import Task
from implementation.predictors.transformers.transformers_model import (
    TransformersModel,
    TransformersModelConfig,
    TransformersModelInput,
    TransformersModelOutput
)
from implementation.tasks.image_classification.actions import (
    ImageClassificationPreprocessor,
    ImageClassificationSingleLabelPostprocessor
)

class TransformersVisualQandAInput(Input):
    def __init__(self, image: Image.Image, question: str, *_: Any, **__: Any):
        self.image: Image.Image = image
        self.question: str = question


    def __setattr__(self, name: str, value: Any) -> None: # disable pydantic
        self.__dict__[name] = value


    def model_dump(
        self, 
        *, 
        mode: str="python", 
        include: Optional[Union[
            set[int], set[str], dict[int, Any], dict[str, Any]
        ]]=None,
        exclude: Optional[Union[
            set[int], set[str], dict[int, Any], dict[str, Any]
        ]]=None,
        by_alias: bool=False, 
        exclude_unset: bool=False,
        exclude_defaults: bool=False,
        exclude_none: bool=False, 
        round_trip: bool=False,
        warnings: bool=True
    ) -> Dict[str, Any]:
        return {
            "image": self.image,
            "question": self.question
        }


class TransformersVisualQandAOutput(Output):
    outputs: Any


class TransformersVisualQandA(
    Task[
        Config,
        TransformersVisualQandAInput, 
        TransformersVisualQandAOutput,
        TransformersModelConfig,
        TransformersModelInput,
        TransformersModelOutput
    ]
):
    input_class: Type[TransformersVisualQandAInput] = TransformersVisualQandAInput
    output_class: Type[TransformersVisualQandAOutput] = TransformersVisualQandAOutput
    
    def __init__(
        self,
        *,
        cfg: Optional[Config] = None, 
        predictor: TransformersModel,
        preprocess: Optional[List[Action[InputState, OutputState]]]=None,
        postprocess: Optional[List[Action[InputState, OutputState]]]=None
    ) -> None:
        self.cfg = cfg
        self.predictor = predictor
        self._preprocess = preprocess or [ImageClassificationPreprocessor()]
        self._postprocess = postprocess or [ImageClassificationSingleLabelPostprocessor()]