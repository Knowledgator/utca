from typing import Any, List, Type, Optional

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
from implementation.tasks.text_processing.textual_q_and_a.transformers.actions import (
    QandAPostprocess
)

class QandAInput(Input):
    question: str
    context: str


class QandAOutput(Output):
    answer: Optional[str]=None
    score: float=0.


class QandATask(
    Task[
        QandAInput, 
        QandAOutput,
    ]
):
    default_model: str = "deepset/roberta-base-squad2"
    
    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[List[Action[Any, Any]]]=None,
        postprocess: Optional[List[Action[Any, Any]]]=None,
        input_class: Type[QandAInput]=QandAInput,
        output_class: Type[QandAOutput]=QandAOutput
    ) -> None:
        if not predictor:
            predictor = TransformersPipeline(
                TransformersPipelineConfig(
                    task="question-answering", 
                    model=self.default_model
                ),
                input_class=QandAInput,
                output_class=QandAOutput
            )

        super().__init__(
            predictor=predictor,
            preprocess=preprocess or [],
            postprocess=postprocess or [QandAPostprocess()],
            input_class=input_class, 
            output_class=output_class,
        )
