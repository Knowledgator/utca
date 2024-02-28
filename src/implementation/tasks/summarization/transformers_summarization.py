from typing import Type, Optional, List, Dict, Any

from core.executable_level_1.schema import (
    Config, Input, Output
)
from core.executable_level_1.actions import (
    Action, InputState, OutputState
)
from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import (
    PredictorConfigType, PredictorInputType, PredictorOutputType
)
from core.task_level_3.task import Task
from implementation.tasks.summarization.actions import (
    SummarizationPostprocess
)

class SummarizationInput(Input):
    inputs: Dict[str, Any]


class SummarizationOutput(Output):
    summary_text: str


class SummarizationTask(
    Task[
        Config,
        SummarizationInput, 
        SummarizationOutput,
    ]
):
    def __init__(
        self,
        *,
        cfg: Optional[Config]=None, 
        predictor: Predictor[
            PredictorConfigType, 
            PredictorInputType, 
            PredictorOutputType
        ],
        preprocess: Optional[List[Action[InputState, OutputState]]]=None,
        postprocess: Optional[List[Action[InputState, OutputState]]]=None,
        input_class: Type[SummarizationInput]=SummarizationInput,
        output_class: Type[SummarizationOutput]=SummarizationOutput
    ) -> None:
        super().__init__(
            cfg=cfg, 
            predictor=predictor,
            preprocess=preprocess or [],
            postprocess=postprocess or [SummarizationPostprocess()],
            input_class=input_class, 
            output_class=output_class,
        )
