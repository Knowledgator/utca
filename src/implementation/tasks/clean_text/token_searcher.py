from typing import Type, Optional, List

from core.executable_level_1.actions import Action, InputState, OutputState
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
    TokenSearcherPredictorConfig, 
    TokenSearcherPredictorInput, 
    TokenSearcherPredictorOutput
)
from implementation.predictors.token_searcher.predictor import (
    TokenSearcherPredictor
)
from implementation.tasks.clean_text.actions import (
    TokenSeatcherTextCleanerPreprocessor,
    TokenSearcherTextCleanerPostprocessor
)

class TokenSearcherTextCleanerInput(InputWithThreshold):
    text: str
    clean: Optional[bool] = None


class TokenSearcherTextCleanerOutput(NEROutput[Entity]):
    text: str
    cleaned_text: Optional[str] = None


class TokenSearcherTextCleanerTask(
    NERTask[
        NERConfig,
        TokenSearcherTextCleanerInput, 
        TokenSearcherTextCleanerOutput,
        TokenSearcherPredictorConfig, 
        TokenSearcherPredictorInput, 
        TokenSearcherPredictorOutput
    ]
):
    input_class: Type[TokenSearcherTextCleanerInput] = TokenSearcherTextCleanerInput
    output_class: Type[TokenSearcherTextCleanerOutput] = TokenSearcherTextCleanerOutput
    
    def __init__(
        self,
        cfg: Optional[NERConfig]=None, 
        predictor: Optional[Predictor[
            TokenSearcherPredictorConfig, 
            TokenSearcherPredictorInput, 
            TokenSearcherPredictorOutput
        ]]=None,
        preprocess: Optional[List[Action[InputState, OutputState]]]=None,
        postprocess: Optional[List[Action[InputState, OutputState]]]=None
    ) -> None:
        self.cfg = cfg or NERConfig()
        self.predictor = predictor or TokenSearcherPredictor()
        self._preprocess = preprocess or [TokenSeatcherTextCleanerPreprocessor()]
        self._postprocess = postprocess or [TokenSearcherTextCleanerPostprocessor()]