from typing import Type, Optional, List

from core.executable_level_1.actions import (
    Action, InputState, OutputState
)
from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import (
    PredictorConfigType, PredictorInputType, PredictorOutputType
)
from core.task_level_3.task import NERTask
from core.task_level_3.schema import (
    InputWithThreshold, 
    NEROutput,
    NERConfig 
)
from core.task_level_3.objects.objects import (
    ClassifiedEntity
)
from implementation.tasks.token_classification.actions import (
    TokenClassifierPostprocessor
)

class TokenClassifierInput(InputWithThreshold):
    inputs: str


class TokenClassifierTask(
    NERTask[
        NERConfig,
        TokenClassifierInput, 
        NEROutput[ClassifiedEntity],
    ]
):
    def __init__(
        self,
        *,
        cfg: Optional[NERConfig]=None, 
        predictor: Predictor[
            PredictorConfigType, 
            PredictorInputType, 
            PredictorOutputType
        ],
        preprocess: Optional[List[Action[InputState, OutputState]]]=None,
        postprocess: Optional[List[Action[InputState, OutputState]]]=None,
        input_class: Type[TokenClassifierInput]=TokenClassifierInput,
        output_class: Type[NEROutput[ClassifiedEntity]]=NEROutput[ClassifiedEntity]
    ) -> None:
        super().__init__(
            cfg=cfg or NERConfig(), 
            predictor=predictor,
            preprocess=preprocess or [],
            postprocess=postprocess or [TokenClassifierPostprocessor()],
            input_class=input_class, 
            output_class=output_class,
        )