from typing import Any, Type, Optional

from utca.core.executable_level_1.component import Component
from utca.core.executable_level_1.schema import Input, Output
from utca.core.predictor_level_2.predictor import Predictor
from utca.core.task_level_3.task import Task
from utca.implementation.predictors.transformers_predictor.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig
)
from utca.implementation.predictors.transformers_predictor.schema import (
    TransformersTextualQandAInput,
    TransformersTextualQandAOutput
)

class TransformersTextualQandA(
    Task[Input, Output]
):
    """
    Textual Q&A task
    """
    default_model: str = "deepset/roberta-base-squad2"
    
    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[Component]=None,
        postprocess: Optional[Component]=None,
        input_class: Type[Input]=TransformersTextualQandAInput,
        output_class: Type[Output]=TransformersTextualQandAOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            predictor (Optional[Predictor[Any, Any]], optional): Predictor that will be used in task. 
                If equals to None, default predictor will be used. Defaults to None.
            
            preprocess (Optional[Component], optional): Component executed
                before predictor. Defaults to None.
            
            postprocess (Optional[Component], optional): Component executed
                after predictor. Defaults to None.
            
            input_class (Type[Input], optional): Class for input validation. 
                Defaults to TransformersTextualQandAInput.
            
            output_class (Type[Output], optional): Class for output validation.
                Defaults to TransformersTextualQandAOutput.
            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        if not predictor:
            predictor = TransformersPipeline(
                TransformersPipelineConfig(
                    task="question-answering", 
                    model=self.default_model
                ),
                input_class=TransformersTextualQandAInput,
                output_class=TransformersTextualQandAOutput
            )

        super().__init__(
            predictor=predictor,
            preprocess=preprocess,
            postprocess=postprocess,
            input_class=input_class, 
            output_class=output_class,
            name=name,
        )
