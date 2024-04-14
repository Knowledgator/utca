from typing import Any, List, Optional, Type

from core.executable_level_1.schema import Input
from core.executable_level_1.actions import (
    Action
)
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.task import NERTask
from core.task_level_3.schema import (
    NEROutput,
)
from core.task_level_3.objects.objects import (
    Entity
)
from implementation.predictors.token_searcher.predictor import (
    TokenSearcherPredictor
)
from implementation.tasks.text_processing.clean_text.token_searcher.actions import (
    TokenSeatcherTextCleanerPreprocessor,
    TokenSearcherTextCleanerPostprocessor
)

class TokenSearcherTextCleanerInput(Input):
    text: str
    clean: Optional[bool] = None


class TokenSearcherTextCleanerOutput(NEROutput[Entity]):
    text: str
    cleaned_text: Optional[str] = None


class TokenSearcherTextCleaner(
    NERTask[
        TokenSearcherTextCleanerInput,
        TokenSearcherTextCleanerOutput
    ]
):

    def __init__(
        self,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[List[Action[Any, Any]]]=None,
        postprocess: Optional[List[Action[Any, Any]]]=None,
        input_class: Type[TokenSearcherTextCleanerInput]=TokenSearcherTextCleanerInput,
        output_class: Type[TokenSearcherTextCleanerOutput]=TokenSearcherTextCleanerOutput
    ) -> None:
        super().__init__(
            predictor=predictor or TokenSearcherPredictor(),
            preprocess=preprocess or [TokenSeatcherTextCleanerPreprocessor()],
            postprocess=postprocess or [TokenSearcherTextCleanerPostprocessor()],
            input_class=input_class,
            output_class=output_class
        )