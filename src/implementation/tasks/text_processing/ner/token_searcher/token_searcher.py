from typing import Any, List, Optional, Type

from core.executable_level_1.actions import Action
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.task import NERTask
from core.task_level_3.schema import (
    InputWithThreshold, 
    NEROutput,
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
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[List[Action[Any, Any]]]=None,
        postprocess: Optional[List[Action[Any, Any]]]=None,
        input_class: Type[TokenSearcherNERInput]=TokenSearcherNERInput,
        output_class: Type[TokenSearcherNEROutput]=TokenSearcherNEROutput
    ) -> None:
        super().__init__(
            predictor=predictor or TokenSearcherPredictor(),
            preprocess=preprocess or [TokenSearcherNERPreprocessor()],
            postprocess=postprocess or [TokenSearcherNERPostprocessor()],
            input_class=input_class,
            output_class=output_class
        )