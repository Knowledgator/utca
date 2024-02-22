from typing import Any, Dict, List, Type

from transformers import ( # type: ignore
    pipeline, Pipeline # type: ignore
)

from core.executable_level_1.schema import Input, Output
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


class TransformersTextToSpeechInput(Input):
    text: str


class TransformersTextToSpeechOutput(Output):
    text: str
    outputs: Dict[str, Any]


class TransformersTextToSpeechPipeline(
    TransformersPipeline[
        TransformersTextToSpeechConfig,
        TransformersTextToSpeechInput,
        TransformersTextToSpeechOutput,
    ]
):
    input_class: Type[TransformersTextToSpeechInput] = TransformersTextToSpeechInput
    output_class: Type[TransformersTextToSpeechOutput] = TransformersTextToSpeechOutput

    def __init__(self, cfg: TransformersTextToSpeechConfig) -> None:
        self.pipeline = cfg.pipeline 
        super().__init__(cfg)


    def get_predictions(self, inputs: Any) -> Any:
        return self.pipeline( # type: ignore
            inputs,
            forward_params={"do_sample": True}
        )
    

    def invoke(self, input_data: TransformersTextToSpeechInput) -> Dict[str, Any]:
        return {
            'text': input_data.text,
            'outputs': self.get_predictions(input_data.text)
        }
    

    def invoke_batch(
        self, input_data: List[TransformersTextToSpeechInput]
    ) -> List[Dict[str, Any]]:
        raise Exception('TODO!')