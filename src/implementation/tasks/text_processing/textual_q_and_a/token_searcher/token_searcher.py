from typing import Any, List, Type, Optional

from core.executable_level_1.schema import IOModel
from core.executable_level_1.actions import Action
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.task import NERTask
from core.task_level_3.schema import ( 
    NEROutput 
)
from core.task_level_3.objects.objects import (
    Entity
)
from implementation.predictors.token_searcher.predictor import (
    TokenSearcherPredictor
)
from implementation.tasks.text_processing.textual_q_and_a.token_searcher.actions import (
    TokenSearcherQandAPreprocessor,
    TokenSearcherQandAPostprocessor
)

class TokenSearcherQandAInput(IOModel):
    question: str
    text: str


class TokenSearcherQandAOutput(NEROutput[Entity]):
    text: str
    question: str


class TokenSearcherQandATask(
    NERTask[
        TokenSearcherQandAInput, 
        TokenSearcherQandAOutput
    ]
):
    
    def __init__(
        self,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[List[Action[Any, Any]]]=None,
        postprocess: Optional[List[Action[Any, Any]]]=None,
        input_class: Type[TokenSearcherQandAInput]=TokenSearcherQandAInput,
        output_class: Type[TokenSearcherQandAOutput]=TokenSearcherQandAOutput,
        name: Optional[str]=None,
    ) -> None:
        super().__init__(
            predictor=predictor or TokenSearcherPredictor(),
            preprocess=preprocess or [TokenSearcherQandAPreprocessor()],
            postprocess=postprocess or [TokenSearcherQandAPostprocessor()],
            input_class=input_class,
            output_class=output_class,
            name=name,
        )