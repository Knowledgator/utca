from typing import Any, Optional, Type

from utca.core.executable_level_1.component import Component
from utca.core.executable_level_1.schema import Input, Output
from utca.core.predictor_level_2.predictor import Predictor
from utca.core.task_level_3.task import Task
from utca.implementation.predictors.transformers_predictor.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig,
)
from utca.implementation.predictors.transformers_predictor.schema import (
    TransformersBasicInput,
    TransformersBasicOutput
)

class TransformersTextClassification(
    Task[Input, Output]
):
    """
    Task for text classification
    """

    default_model: str = "ProsusAI/finbert"

    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[Component]=None,
        postprocess: Optional[Component]=None,
        input_class: Type[Input]=TransformersBasicInput,
        output_class: Type[Output]=TransformersBasicOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            predictor (Optional[Predictor[Any, Any]]): Predictor that will be used in task. 
                If equals to None, default ComprehendItPredictor will be used. Defaults to None.

            preprocess (Optional[Component]): Chain of actions executed 
                before predictor. Defaults to None.
            
            postprocess (Optional[Component]): Chain of actions executed
                after predictor. Defaults to None.
            
            input_class (Type[Input]): Class for input validation. Defaults to ComprehendItPredictorInput.

            output_class (Type[Output]): Class for output validation. Defaults to ComprehendItPredictorOutput.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        if not predictor:
            predictor = TransformersPipeline(
                TransformersPipelineConfig(
                    task="text-classification", 
                    model=self.default_model,
                    kwargs={"top_k": None}
                ),
                input_class=TransformersBasicInput,
                output_class=TransformersBasicOutput
            )

        super().__init__(
            predictor=predictor,
            preprocess=preprocess,
            postprocess=postprocess,
            input_class=input_class, 
            output_class=output_class,
            name=name,
        )

