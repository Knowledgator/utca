from typing import TypeVar, Any, Type, Dict, Optional

from transformers import PreTrainedModel # type: ignore

from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.schema import (
    Config, InputType, OutputType
)
from core.predictor_level_2.predictor import Predictor

class TransformersModelConfig(Config):
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
        InputType, 
        OutputType
    ]
):
   
    def __init__(
        self, 
        cfg: TransformersModelConfig,
        input_class: Type[InputType],
        output_class: Type[OutputType]
    ) -> None:
        self.cfg = cfg
        super().__init__(input_class, output_class)


    def invoke(self, input_data: InputType, evaluator: Evaluator) -> Dict[str, Any]:
        inputs = input_data.model_dump()
        if not "encodings" in inputs:
            res = self.cfg.model(**inputs, **self.cfg.get_kwargs())
        else:
            res = self.cfg.model(**inputs.pop("encodings"), **inputs, **self.cfg.get_kwargs())
        return self.ensure_dict(res)


    @property
    def config(self) -> Any:
        return self.cfg.model.config # type: ignore


class TransformersGenerativeModel(
    TransformersModel[
        InputType, 
        OutputType
    ]
):
    def invoke(self, input_data: InputType, evaluator: Evaluator) -> Dict[str, Any]:
        inputs = input_data.model_dump()
        if not "encodings" in inputs:
            res = self.cfg.model.generate(**inputs, **self.cfg.get_kwargs()) # type: ignore
        else:
            res = self.cfg.model.generate(**inputs.pop("encodings"), **inputs, **self.cfg.get_kwargs()) # type: ignore
        return self.ensure_dict(res)