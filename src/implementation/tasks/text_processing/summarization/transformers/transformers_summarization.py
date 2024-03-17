from typing import Any, Type, Optional, List

from implementation.predictors.transformers.transformers_pipeline import (
    TransformersSummarizationPipeline,
    TransformersPipelineConfig,
    SummarizationInput
)

from core.executable_level_1.schema import (
    Output
)
from core.executable_level_1.actions import (
    Action, ActionInput, ActionOutput
)
from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import (
    PredictorInput,
    PredictorOutput
)
from core.task_level_3.task import Task
from implementation.tasks.text_processing.summarization.transformers.actions import (
    SummarizationPostprocess
)

class SummarizationTaskInput(SummarizationInput):
    inputs: str


class SummarizationOutput(Output):
    summary_text: str


class ModelOutput(PredictorOutput):
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
        predictor: Optional[Predictor[
            PredictorInput, 
            PredictorOutput
        ]]=None,
        preprocess: Optional[List[Action[ActionInput, ActionOutput]]]=None,
        postprocess: Optional[List[Action[ActionInput, ActionOutput]]]=None,
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
            postprocess=postprocess or [SummarizationPostprocess()], # type: ignore
            input_class=input_class, 
            output_class=output_class,
        )