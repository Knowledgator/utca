from typing import Type, Optional, List, Any

from core.executable_level_1.schema import (
    Input, Output
)
from core.executable_level_1.actions import Action
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.task import Task
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig
)

class TransformersTextToSpeechInput(Input):
    text_inputs: str


class TransformersTextToSpeechOutput(Output):
    audio: Any
    sampling_rate: int


class TransformersTextToSpeech(
    Task[
        TransformersTextToSpeechInput, 
        TransformersTextToSpeechOutput,
    ]
):
    default_model: str = "suno/bark-small"

    def __init__(
        self, 
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[List[Action[Any, Any]]]=None,
        postprocess: Optional[List[Action[Any, Any]]]=None,
        input_class: Type[TransformersTextToSpeechInput]=TransformersTextToSpeechInput,
        output_class: Type[TransformersTextToSpeechOutput]=TransformersTextToSpeechOutput
    ) -> None:
        super().__init__(
            predictor=(predictor or TransformersPipeline(
                cfg=TransformersPipelineConfig(
                    task="text-to-speech",
                    model=self.default_model,
                    model_kwargs={
                        "do_sample": True
                    }
                ),
                input_class=TransformersTextToSpeechInput,
                output_class=TransformersTextToSpeechOutput
            )),
            preprocess=preprocess or [],
            postprocess=postprocess or [],
            input_class=input_class, 
            output_class=output_class
        )