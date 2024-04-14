from typing import Any, List, Type, Optional

from core.executable_level_1.schema import Input
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

class TokenSearcherQandAInput(Input):
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
        output_class: Type[TokenSearcherQandAOutput]=TokenSearcherQandAOutput
    ) -> None:
        self.predictor = predictor or TokenSearcherPredictor()
        self._preprocess = preprocess or [TokenSearcherQandAPreprocessor()]
        self._postprocess = postprocess or [TokenSearcherQandAPostprocessor()]
        self.input_class = input_class
        self.output_class = output_class