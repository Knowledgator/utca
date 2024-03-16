from typing import Type, Optional, List, Any

from core.executable_level_1.actions import (
    Action, ActionInput, ActionOutput
)
from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import (
    PredictorInput, PredictorOutput
)
from core.task_level_3.task import Task
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig
)

class TransformersTextToSpeechInput(PredictorInput):
    text_inputs: str


class TransformersTextToSpeechOutput(PredictorOutput):
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
        predictor: Optional[Predictor[
            PredictorInput, 
            PredictorOutput
        ]]=None,
        preprocess: Optional[List[Action[ActionInput, ActionOutput]]]=None,
        postprocess: Optional[List[Action[ActionInput, ActionOutput]]]=None,
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
            postprocess=postprocess or [], # type: ignore
            input_class=input_class, 
            output_class=output_class
        )