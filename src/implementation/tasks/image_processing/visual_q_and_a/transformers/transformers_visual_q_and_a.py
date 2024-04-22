from typing import Any, Dict, List, Optional, Tuple, Type

from transformers import ( # type: ignore
    ViltProcessor, ViltForQuestionAnswering, AutoConfig
)

from core.executable_level_1.schema import IOModel
from core.executable_level_1.actions import Action
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.task import Task
from implementation.predictors.transformers.transformers_model import (
    TransformersModel,
    TransformersModelConfig
)
from implementation.predictors.transformers.schema import (
    TransformersVisualQandAInput,
    TransformersImageModelRawInput,
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
    Task[
        TransformersVisualQandAInput, 
        TransformersVisualQandAOutput
    ]
):
    default_model = "dandelin/vilt-b32-finetuned-vqa"
    
    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[List[Action[Any, Any]]]=None,
        postprocess: Optional[List[Action[Any, Any]]]=None,
        input_class: Type[TransformersVisualQandAInput]=TransformersVisualQandAInput,
        output_class: Type[TransformersVisualQandAOutput]=TransformersVisualQandAOutput,
        name: Optional[str]=None,
    ) -> None:
        if not predictor:
            model = ViltForQuestionAnswering.from_pretrained(self.default_model) # type: ignore
            predictor = TransformersModel(
                TransformersModelConfig(
                    model=model # type: ignore
                ),
                input_class=TransformersImageModelRawInput,
                output_class=TransformersLogitsOutput
            )

        if not preprocess:
            processor = ViltProcessor.from_pretrained(self.default_model) # type: ignore
            preprocess=[
                VisualQandAPreprocessor(
                    processor=processor # type: ignore
                )
            ]
        
        if not postprocess:
            labels = AutoConfig.from_pretrained(self.default_model).id2label # type: ignore
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