from typing import List, Optional, Type

from core.executable_level_1.schema import (
    InputType, 
    OutputType,
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
from implementation.predictors.comprehend_it.predictor import (
    ComprehendItPredictor, 
    ComprehendItPredictorInput, 
    ComprehendItPredictorOutput
)

class ComprehendIt(
    Task[
        InputType,
        OutputType
    ]
):
    def __init__(
        self,
        *,
        predictor: Optional[Predictor[
            PredictorInput, 
            PredictorOutput
        ]]=None,
        preprocess: Optional[List[Action[ActionInput, ActionOutput]]]=None,
        postprocess: Optional[List[Action[ActionInput, ActionOutput]]]=None,
        input_class: Type[InputType]=ComprehendItPredictorInput,
        output_class: Type[OutputType]=ComprehendItPredictorOutput
    ) -> None:
        if not predictor:
            predictor = ComprehendItPredictor()

        super().__init__(
            predictor=predictor,
            preprocess=preprocess or [],
            postprocess=postprocess or [],
            input_class=input_class, 
            output_class=output_class,
        )

