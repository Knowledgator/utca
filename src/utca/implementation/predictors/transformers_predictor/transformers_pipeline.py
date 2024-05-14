from typing import Any, Dict, Type, Optional

from transformers import ( # type: ignore
    pipeline, # type: ignore
    Pipeline,
)

from utca.core.executable_level_1.interpreter import Evaluator
from utca.core.executable_level_1.schema import (
    Input, Output
)
from utca.core.predictor_level_2.predictor import Predictor
from utca.implementation.predictors.transformers_predictor.schema import (
    TransformersPipelineConfig, #SummarizationInputType
)
from utca.implementation.predictors.utils import ensure_dict

class TransformersPipeline(
    Predictor[Input, Output]
):
    """
    Transformers pipeline predictor
    """
    pipeline: Pipeline

    def __init__(
        self,
        cfg: TransformersPipelineConfig,
        input_class: Type[Input],
        output_class: Type[Output],
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            cfg (TransformersPipelineConfig): Configuration for predictor.

            input_class (Type[Input]): Class for input validation.

            output_class (Type[Output]): Class for output validation.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        self.pipeline: Pipeline = pipeline(
            **cfg.pipeline_config
        )
        super().__init__(
            input_class=input_class, 
            output_class=output_class, 
            name=name,
        )


    def invoke(self, input_data: Input, evaluator: Evaluator) -> Dict[str, Any]:
        """
        Call pipeline

        Args:
            input_data (Input): Validated input.

            evaluator (Evaluator): Evaluator in context of wich executed.

        Returns:
            Dict[str, Any]: Result of execution.
        """
        inputs = input_data.extract()
        if "inputs" in inputs:
            return ensure_dict(self.pipeline( # type: ignore
                inputs.pop("inputs"), **inputs
            ))
        return ensure_dict(self.pipeline(**inputs)) # type: ignore
    

    @property
    def config(self) -> Any:
        """
        Model configuration
        """
        return self.pipeline.model.config # type: ignore