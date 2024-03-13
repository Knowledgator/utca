from typing import Optional, List, Type

from core.executable_level_1.actions import (
    Action, ActionInput, ActionOutput
)
from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import PredictorInput, PredictorOutput
from core.task_level_3.task import NERTask
from core.task_level_3.schema import (
    InputWithThreshold, 
    NEROutput,
    NERConfig 
)
from core.task_level_3.objects.objects import (
    ClassifiedEntity
)
from implementation.predictors.token_searcher.predictor import (
    TokenSearcherPredictor
)
from implementation.tasks.text_processing.ner.token_searcher.actions import (
    TokenSearcherNERPreprocessor,
    TokenSearcherNERPostprocessor
)

class TokenSearcherNERInput(InputWithThreshold):
    text: str
    labels: list[str]


class TokenSearcherNEROutput(NEROutput[ClassifiedEntity]):
    text: str


class TokenSearcherNERTask(
    NERTask[
        TokenSearcherNERInput, 
        TokenSearcherNEROutput
    ]
):
    def __init__(
        self,
        cfg: Optional[NERConfig]=None, 
        predictor: Optional[Predictor[
            PredictorInput, 
            PredictorOutput
        ]]=None,
        preprocess: Optional[List[Action[ActionInput, ActionOutput]]]=None,
        postprocess: Optional[List[Action[ActionInput, ActionOutput]]]=None,
        input_class: Type[TokenSearcherNERInput]=TokenSearcherNERInput,
        output_class: Type[TokenSearcherNEROutput]=TokenSearcherNEROutput
    ) -> None:
        super().__init__(
            predictor=predictor or TokenSearcherPredictor(),
            preprocess=preprocess or [TokenSearcherNERPreprocessor()], # type: ignore
            postprocess=postprocess or [TokenSearcherNERPostprocessor()], # type: ignore
            input_class=input_class,
            output_class=output_class
        )