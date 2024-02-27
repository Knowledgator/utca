from typing import Any, Dict, Type

from transformers import ( # type: ignore
    pipeline, Pipeline # type: ignore
)

from core.predictor_level_2.schema import (
    PredictorInput, PredictorOutput
)
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipelineConfig,
    TransformersPipeline
)


class TransformersTextToSpeechConfig(TransformersPipelineConfig):    
    def __init__(self, **kwargs: Any):
        self.pipeline: Pipeline = pipeline(
            task='text-to-speech',
            **kwargs
        ) # type: ignore


    def __setattr__(self, name: str, value: Any) -> None: # disable pydantic
        self.__dict__[name] = value


class TransformersTextToSpeechInput(PredictorInput):
    inputs: str


class TransformersTextToSpeechOutput(PredictorOutput):
    inputs: str
    outputs: Dict[str, Any]


class TransformersTextToSpeechPipeline(
    TransformersPipeline[
        TransformersTextToSpeechConfig,
        TransformersTextToSpeechInput,
        TransformersTextToSpeechOutput,
    ]
):
    
    def __init__(
        self, 
        cfg: TransformersTextToSpeechConfig,
        input_class: Type[TransformersTextToSpeechInput]=TransformersTextToSpeechInput,
        output_class: Type[TransformersTextToSpeechOutput]=TransformersTextToSpeechOutput
    ) -> None:
        super().__init__(cfg, input_class, output_class)


    def get_predictions(self, inputs: Any) -> Any:
        return self.pipeline( # type: ignore
            inputs,
            forward_params={"do_sample": True}
        )