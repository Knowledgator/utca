from typing import Type, Optional, Any

from utca.core.executable_level_1.component import Component
from utca.core.executable_level_1.schema import Input, Output
from utca.core.predictor_level_2.predictor import Predictor
from utca.core.task_level_3.task import Task
from utca.implementation.predictors.transformers_predictor.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig
)
from utca.implementation.predictors.transformers_predictor.schema import (
    TransformersTextToSpeechInput,
    TransformersTextToSpeechOutput,
)


class TransformersTextToSpeech(
    Task[Input, Output]
):
    """
    Text to speech task
    """
    default_model: str = "suno/bark-small"

    def __init__(
        self, 
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[Component]=None,
        postprocess: Optional[Component]=None,
        input_class: Type[Input]=TransformersTextToSpeechInput,
        output_class: Type[Output]=TransformersTextToSpeechOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            predictor (Predictor[Any, Any], optional): Predictor that will be used in task. 
                If equals to None, default predictor will be used. Defaults to None.
            
            preprocess (Optional[Component], optional): Component executed
                before predictor. Defaults to None.
            
            postprocess (Optional[Component], optional): Component executed
                after predictor. Defaults to None.
            
            input_class (Type[Input], optional): Class for input validation. 
                Defaults to TransformersTextToSpeechInput.
            
            output_class (Type[Output], optional): Class for output validation.
                Defaults to TransformersTextToSpeechOutput.
            
            name (Optional[str], optional): Name for identification. If equals to None, 
                class name will be used. Defaults to None.
        """
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
            preprocess=preprocess,
            postprocess=postprocess,
            input_class=input_class, 
            output_class=output_class,
            name=name,
        )