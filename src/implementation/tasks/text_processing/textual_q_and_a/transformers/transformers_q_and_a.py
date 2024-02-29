from typing import Type, Optional, List, Any

from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig
)

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
from implementation.tasks.text_processing.textual_q_and_a.transformers.actions import (
    QandAPostprocess
)

class QandAInput(PredictorInput):
    question: str
    context: str


class QandAOutput(Output):
    answer: Any


class QandATask(
    Task[
        Config,
        QandAInput, 
        QandAOutput,
    ]
):
    default_model: str = "deepset/roberta-base-squad2"
    
    def __init__(
        self,
        *,
        cfg: Optional[Config]=None, 
        predictor: Optional[Predictor[
            PredictorConfig, 
            PredictorInput, 
            PredictorOutput
        ]]=None,
        preprocess: Optional[List[Action[InputState, OutputState]]]=None,
        postprocess: Optional[List[Action[InputState, OutputState]]]=None,
        input_class: Type[QandAInput]=QandAInput,
        output_class: Type[QandAOutput]=QandAOutput
    ) -> None:
        if not predictor:
            predictor = TransformersPipeline(
                TransformersPipelineConfig(
                    task="question-answering", 
                    model=self.default_model
                ),
                input_class=QandAInput
            )

        super().__init__(
            cfg=cfg, 
            predictor=predictor,
            preprocess=preprocess or [],
            postprocess=postprocess or [QandAPostprocess()],
            input_class=input_class, 
            output_class=output_class,
        )
