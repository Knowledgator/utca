from typing import Any, Type, Optional, List

from implementation.predictors.transformers.transformers_pipeline import (
    TransformersSummarizationPipeline,
    TransformersPipelineConfig,
    SummarizationInput
)

from core.executable_level_1.schema import (
    Input, Output
)
from core.executable_level_1.actions import Action
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.task import Task
from implementation.tasks.text_processing.summarization.transformers.actions import (
    SummarizationPostprocess
)

class SummarizationTaskInput(SummarizationInput):
    inputs: str


class SummarizationOutput(Output):
    summary_text: str


class ModelOutput(Output):
    output: Any


class SummarizationTask(
    Task[
        SummarizationTaskInput, 
        SummarizationOutput,
    ]
):
    default_model = "facebook/bart-large-cnn"

    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Input, Output]]=None,
        preprocess: Optional[List[Action[Any, Any]]]=None,
        postprocess: Optional[List[Action[Any, Any]]]=None,
        input_class: Type[SummarizationTaskInput]=SummarizationTaskInput,
        output_class: Type[SummarizationOutput]=SummarizationOutput
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
                input_class=SummarizationTaskInput,
                output_class=ModelOutput
            )

        super().__init__(
            predictor=predictor,
            preprocess=preprocess or [],
            postprocess=postprocess or [SummarizationPostprocess()],
            input_class=input_class, 
            output_class=output_class,
        )