from typing import Type, Optional, List, Any

from core.executable_level_1.schema import (
    Config, Output
)
from core.executable_level_1.actions import (
    Action, InputState, OutputState
)
from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import (
    PredictorConfig, PredictorInput, PredictorOutput
)
from core.task_level_3.task import Task
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig
)
from implementation.tasks.audio_processing.text_to_speech.transformers.actions import (
    TextToSpeechPostprocess
)

class TransformersTextToSpeechInput(PredictorInput):
    text_inputs: str


class TransformersTextToSpeechOutput(Output):
    audio_data: Any
    sampling_rate: int


class TransformersTextToSpeech(
    Task[
        Config,
        TransformersTextToSpeechInput, 
        TransformersTextToSpeechOutput,
    ]
):
    default_model: str = "suno/bark-small"

    def __init__(
        self, 
        cfg: Optional[Config]=None,
        predictor: Optional[Predictor[
            PredictorConfig, 
            PredictorInput, 
            PredictorOutput
        ]]=None,
        preprocess: Optional[List[Action[InputState, OutputState]]]=None,
        postprocess: Optional[List[Action[InputState, OutputState]]]=None,
        input_class: Type[TransformersTextToSpeechInput]=TransformersTextToSpeechInput,
        output_class: Type[TransformersTextToSpeechOutput]=TransformersTextToSpeechOutput
    ) -> None:
        super().__init__(
            cfg=cfg,
            predictor=(predictor or TransformersPipeline(
                cfg=TransformersPipelineConfig(
                    task="text-to-speech",
                    model=self.default_model,
                    model_kwargs={
                        "do_sample": True
                    }
                ),
                input_class=TransformersTextToSpeechInput,
            )),
            preprocess=preprocess or [],
            postprocess=postprocess or [TextToSpeechPostprocess()],
            input_class=input_class, 
            output_class=output_class
        )