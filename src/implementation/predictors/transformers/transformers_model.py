from typing import Any, Dict, Type, TypeVar, Optional

from pydantic import ConfigDict
from transformers import PreTrainedModel # type: ignore

from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.schema import (
    Config, Input, Output
)
from core.predictor_level_2.predictor import Predictor
from implementation.predictors.transformers.utils import ensure_dict

class TransformersModelConfig(Config):
    model_config = ConfigDict(arbitrary_types_allowed=True)

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
        Input, 
        Output
    ]
):
   
    def __init__(
        self, 
        cfg: TransformersModelConfig,
        input_class: Type[Input],
        output_class: Type[Output],
        name: Optional[str]=None,
    ) -> None:
        super().__init__(
            input_class=input_class,
            output_class=output_class,
            name=name,
        )
        self.cfg = cfg


    def invoke(self, input_data: Input, evaluator: Evaluator) -> Dict[str, Any]:
        inputs = input_data.extract()
        if not "encodings" in inputs:
            res = self.cfg.model(**inputs, **self.cfg.get_kwargs())
        else:
            res = self.cfg.model(**inputs.pop("encodings"), **inputs, **self.cfg.get_kwargs())
        return ensure_dict(res)


    @property
    def config(self) -> Any:
        return self.cfg.model.config # type: ignore


class TransformersGenerativeModel(
    TransformersModel[
        Input, 
        Output
    ]
):
    def invoke(self, input_data: Input, evaluator: Evaluator) -> Dict[str, Any]:
        inputs = input_data.extract()
        if not "encodings" in inputs:
            res = self.cfg.model.generate(**inputs, **self.cfg.get_kwargs()) # type: ignore
        else:
            res = self.cfg.model.generate(**inputs.pop("encodings"), **inputs, **self.cfg.get_kwargs()) # type: ignore
        return ensure_dict(res)