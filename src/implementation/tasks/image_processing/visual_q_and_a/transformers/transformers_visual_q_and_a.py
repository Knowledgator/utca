from typing import Any, Dict, List, Optional, Tuple, Type

from transformers import ( # type: ignore
    ViltProcessor, ViltForQuestionAnswering
)

from core.executable_level_1.schema import IOModel, Input, Output
from core.executable_level_1.executor import ActionType
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.task import Task
from implementation.predictors.transformers.transformers_model import (
    TransformersModel,
    TransformersModelConfig
)
from implementation.predictors.transformers.schema import (
    TransformersVisualQandAInput,
    TransformersImageModelInput,
    TransformersLogitsOutput
)
from implementation.tasks.image_processing.visual_q_and_a.transformers.actions import (
    VisualQandAPreprocessor,
    VisualQandASingleAnswerPostprocessor,
)

class TransformersVisualQandAOutput(IOModel):
    answer: Tuple[str, float]


class TransformersVisualQandAMultianswerOutput(IOModel):
    answers: Dict[str, float]


class TransformersVisualQandA(
    Task[Input, Output]
):
    """
    Visual Q&A task
    """
    default_model = "dandelin/vilt-b32-finetuned-vqa"
    
    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[List[ActionType]]=None,
        postprocess: Optional[List[ActionType]]=None,
        input_class: Type[Input]=TransformersVisualQandAInput,
        output_class: Type[Output]=TransformersVisualQandAOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            predictor (Predictor[Any, Any], optional): Predictor that will be used in task. 
                If equals to None, default predictor will be used. Defaults to None.
            
            preprocess (Optional[List[Action[Any, Any]]], optional): Chain of actions executed
                before predictor. If equals to None, default chain will be used. Defaults to None.

                Default chain: 
                    [VisualQandAPreprocessor]

                If default chain is used, VisualQandAPreprocessor will use ViltProcessor 
                    from "dandelin/vilt-b32-finetuned-vqa" model.
            
            postprocess (Optional[List[Action[Any, Any]]], optional): Chain of actions executed
                after predictor. If equals to None, default chain will be used. Defaults to None.

                Default chain: 
                    [VisualQandASingleAnswerPostprocessor]

                If default chain is used, VisualQandASingleAnswerPostprocessor will use labels 
                from "dandelin/vilt-b32-finetuned-vqa" model.

            input_class (Type[Input], optional): Class for input validation. 
                Defaults to TransformersVisualQandAInput.
            
            output_class (Type[Output], optional): Class for output validation. 
                Defaults to TransformersVisualQandAOutput.
            
            name (Optional[str], optional): Name for identification. If equals to None, 
                class name will be used. Defaults to None.
        """
        if not predictor:
            model = ViltForQuestionAnswering.from_pretrained(self.default_model) # type: ignore
            predictor = TransformersModel(
                TransformersModelConfig(
                    model=model # type: ignore
                ),
                input_class=TransformersImageModelInput,
                output_class=TransformersLogitsOutput
            )

        if not preprocess:
            processor = ViltProcessor.from_pretrained(predictor.config._name_or_path) # type: ignore
            preprocess=[
                VisualQandAPreprocessor(
                    processor=processor # type: ignore
                )
            ]
        
        if not postprocess:
            labels = predictor.config.id2label # type: ignore
            postprocess=[ # type: ignore
                VisualQandASingleAnswerPostprocessor(
                    labels=labels # type: ignore
                )
            ]

        super().__init__(
            predictor=predictor,
            preprocess=preprocess,
            postprocess=postprocess,
            input_class=input_class, 
            output_class=output_class,
            name=name,
        )