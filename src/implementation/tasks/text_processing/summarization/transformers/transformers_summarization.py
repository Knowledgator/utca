from typing import Any, Type, Optional, List

from core.executable_level_1.schema import Output
from core.executable_level_1.actions import Action
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.task import Task
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersSummarizationPipeline,
    TransformersPipelineConfig,
)
from implementation.predictors.transformers.schema import (
    TransformersBasicInput,
    TransformersBasicOutput
)
from implementation.tasks.text_processing.summarization.transformers.actions import (
    SummarizationPostprocess
)

class SummarizationOutput(Output):
    summary_text: str


class TransformersTextSummarization(
    Task[
        TransformersBasicInput, 
        SummarizationOutput,
    ]
):
    default_model = "facebook/bart-large-cnn"

    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[List[Action[Any, Any]]]=None,
        postprocess: Optional[List[Action[Any, Any]]]=None,
        input_class: Type[TransformersBasicInput]=TransformersBasicInput,
        output_class: Type[SummarizationOutput]=SummarizationOutput,
        name: Optional[str]=None,
    ) -> None:
        if not predictor:
            predictor = TransformersSummarizationPipeline(
                TransformersPipelineConfig(
                    task="summarization", 
                    model=self.default_model,
                    kwargs={
                        "truncation": True
                    }
                ),
                input_class=TransformersBasicInput,
                output_class=TransformersBasicOutput
            )

        super().__init__(
            predictor=predictor,
            preprocess=preprocess or [],
            postprocess=postprocess or [SummarizationPostprocess()],
            input_class=input_class, 
            output_class=output_class,
            name=name,
        )