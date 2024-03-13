from typing import Type, Optional, Any, List

from PIL import Image
from transformers import ( # type: ignore
    ViltProcessor, ViltForQuestionAnswering, AutoConfig
)

from core.executable_level_1.schema import Input, Output
from core.executable_level_1.actions import (
    Action, ActionInput, ActionOutput
)
from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import (
    PredictorInput, PredictorOutput
)
from core.task_level_3.task import Task
from implementation.predictors.transformers.transformers_model import (
    TransformersModel,
    TransformersModelConfig
)
from implementation.tasks.image_processing.visual_q_and_a.transformers.actions import (
    VisualQandAPreprocessor,
    VisualQandAPreprocessorConfig,
    VisualQandAPostprocessor,
    VisualQandAPostprocessorConfig
)

class TransformersVisualQandAInput(Input):
    class Config:
        arbitrary_types_allowed = True
        
    image: Image.Image
    question: str


class TransformersVisualQandAOutput(Output):
    answer: str


class ModelInput(PredictorInput):
    input_ids: Any
    token_type_ids: Any
    attention_mask: Any
    pixel_values: Any
    pixel_mask: Any


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
        predictor: Optional[Predictor[
            PredictorInput, 
            PredictorOutput
        ]]=None,
        preprocess: Optional[List[Action[ActionInput, ActionOutput]]]=None,
        postprocess: Optional[List[Action[ActionInput, ActionOutput]]]=None,
        input_class: Type[TransformersVisualQandAInput]=TransformersVisualQandAInput,
        output_class: Type[TransformersVisualQandAOutput]=TransformersVisualQandAOutput
    ) -> None:
        if not predictor:
            model = ViltForQuestionAnswering.from_pretrained(self.default_model) # type: ignore
            predictor = TransformersModel(
                TransformersModelConfig(
                    model=model # type: ignore
                ),
                input_class=ModelInput
            )

        if not preprocess:
            processor = ViltProcessor.from_pretrained(self.default_model) # type: ignore
            preprocess=[ # type: ignore
                VisualQandAPreprocessor(
                    VisualQandAPreprocessorConfig(
                        processor=processor # type: ignore
                    )
                )
            ]
        
        if not postprocess:
            labels = AutoConfig.from_pretrained(self.default_model).id2label # type: ignore
            postprocess=[ # type: ignore
                VisualQandAPostprocessor(
                    VisualQandAPostprocessorConfig(
                        labels=labels # type: ignore
                    )
                )
            ]

        super().__init__(
            predictor=predictor, # type: ignore
            preprocess=preprocess,
            postprocess=postprocess,
            input_class=input_class, 
            output_class=output_class
        )