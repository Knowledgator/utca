from typing import Type, Optional, List

from core.executable_level_1.actions import (
    Action, ActionInput, ActionOutput
)
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.task import NERTask
from core.task_level_3.schema import (
    InputWithThreshold, 
    NEROutput,
    NERConfig 
)
from core.task_level_3.objects.objects import (
    Entity
)
from implementation.predictors.token_searcher.schema import (
    TokenSearcherPredictorInput, 
    TokenSearcherPredictorOutput
)
from implementation.predictors.token_searcher.predictor import (
    TokenSearcherPredictor
)
from implementation.tasks.text_processing.textual_q_and_a.token_searcher.actions import (
    TokenSearcherQandAPreprocessor,
    TokenSearcherQandAPostprocessor
)

class TokenSearcherQandAInput(InputWithThreshold):
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
        cfg: Optional[NERConfig]=None, 
        predictor: Optional[Predictor[
            TokenSearcherPredictorInput, 
            TokenSearcherPredictorOutput
        ]]=None,
        preprocess: Optional[List[Action[ActionInput, ActionOutput]]]=None,
        postprocess: Optional[List[Action[ActionInput, ActionOutput]]]=None,
        input_class: Type[TokenSearcherQandAInput]=TokenSearcherQandAInput,
        output_class: Type[TokenSearcherQandAOutput]=TokenSearcherQandAOutput
    ) -> None:
        self.cfg = cfg or NERConfig()
        self.predictor = predictor or TokenSearcherPredictor()
        self._preprocess = preprocess or [TokenSearcherQandAPreprocessor()]
        self._postprocess = postprocess or [TokenSearcherQandAPostprocessor()]
        self.input_class = input_class
        self.output_class = output_class