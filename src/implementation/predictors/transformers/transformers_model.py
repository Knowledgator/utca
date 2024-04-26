from typing import Any, Dict, Type, Optional

from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.schema import (
    Input, Output
)
from core.predictor_level_2.predictor import Predictor
from implementation.predictors.transformers.schema import TransformersModelConfig
from implementation.predictors.transformers.utils import ensure_dict

class TransformersModel(
    Predictor[
        Input, 
        Output
    ]
):
    """
    Transformers model predictor
    """
    def __init__(
        self, 
        cfg: TransformersModelConfig,
        input_class: Type[Input],
        output_class: Type[Output],
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            cfg (TransformersModelConfig): Configuration for predictor.

            input_class (Type[Input]): Class for input validation.

            output_class (Type[Output]): Class for output validation.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
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
        """
        Model configuration
        """
        return self.cfg.model.config # type: ignore


class TransformersGenerativeModel(
    TransformersModel[
        Input, 
        Output
    ]
):
    """
    Transformers generative model
    """
    def invoke(self, input_data: Input, evaluator: Evaluator) -> Dict[str, Any]:
        inputs = input_data.extract()
        if not "encodings" in inputs:
            res = self.cfg.model.generate(**inputs, **self.cfg.get_kwargs()) # type: ignore
        else:
            res = self.cfg.model.generate(**inputs.pop("encodings"), **inputs, **self.cfg.get_kwargs()) # type: ignore
        return ensure_dict(res)