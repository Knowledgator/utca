from typing import Any, List, Optional, Type

from core.executable_level_1.actions import Action
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.task import Task
from implementation.predictors.comprehend_it.predictor import (
    ComprehendItPredictor, 
    ComprehendItPredictorInput, 
    ComprehendItPredictorOutput
)

class ComprehendIt(
    Task[
        ComprehendItPredictorInput,
        ComprehendItPredictorOutput
    ]
):
    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[List[Action[Any, Any]]]=None,
        postprocess: Optional[List[Action[Any, Any]]]=None,
        input_class: Type[ComprehendItPredictorInput]=ComprehendItPredictorInput,
        output_class: Type[ComprehendItPredictorOutput]=ComprehendItPredictorOutput,
        name: Optional[str]=None,
    ) -> None:
        if not predictor:
            predictor = ComprehendItPredictor()

        super().__init__(
            predictor=predictor,
            preprocess=preprocess or [],
            postprocess=postprocess or [],
            input_class=input_class, 
            output_class=output_class,
            name=name,
        )

