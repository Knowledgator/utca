from typing import Any, List, Type, Optional

from core.executable_level_1.schema import Input, Output
from core.executable_level_1.executor import ActionType
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.task import Task
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig
)
from implementation.predictors.transformers.schema import (
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
        preprocess: Optional[List[ActionType]]=None,
        postprocess: Optional[List[ActionType]]=None,
        input_class: Type[Input]=TransformersTextualQandAInput,
        output_class: Type[Output]=TransformersTextualQandAOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            predictor (Predictor[Any, Any], optional): Predictor that will be used in task. 
                If equals to None, default predictor will be used. Defaults to None.
            
            preprocess (Optional[List[Action[Any, Any]]], optional): Chain of actions executed
                before predictor. Defaults to None.
            
            postprocess (Optional[List[Action[Any, Any]]], optional): Chain of actions executed
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
            preprocess=preprocess or [],
            postprocess=postprocess or [],
            input_class=input_class, 
            output_class=output_class,
            name=name,
        )
