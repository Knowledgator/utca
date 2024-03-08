from typing import Type, Optional, List, Union

from implementation.predictors.transformers.transformers_pipeline import (
    TransformersSummarizationPipeline,
    TransformersPipelineConfig,
    SummarizationInput
)

from core.executable_level_1.schema import (
    Config, Output
)
from core.executable_level_1.actions import (
    OneToOne, OneToMany, ManyToOne, ManyToMany
)
from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import (
    PredictorConfig,
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


class SummarizationTask(
    Task[
        Config,
        SummarizationTaskInput, 
        SummarizationOutput,
    ]
):
    default_model = "facebook/bart-large-cnn"

    def __init__(
        self,
        *,
        cfg: Optional[Config]=None, 
        predictor: Optional[Predictor[
            PredictorConfig, 
            PredictorInput, 
            PredictorOutput
        ]]=None,
        preprocess: Optional[List[Union[OneToOne, OneToMany, ManyToOne, ManyToMany]]]=None,
        postprocess: Optional[List[Union[OneToOne, OneToMany, ManyToOne, ManyToMany]]]=None,
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
                input_class=SummarizationTaskInput
            )

        super().__init__(
            cfg=cfg, 
            predictor=predictor,
            preprocess=preprocess or [],
            postprocess=postprocess or [SummarizationPostprocess()],
            input_class=input_class, 
            output_class=output_class,
        )