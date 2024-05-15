from typing import Any, Optional, Type

from utca.core.executable_level_1.component import Component
from utca.core.executable_level_1.schema import IOModel, Input
from utca.core.predictor_level_2.predictor import Predictor
from utca.core.task_level_3.task import NERTask
from utca.core.task_level_3.schema import (
    NEROutput, NEROutputType
)
from utca.core.task_level_3.objects.objects import (
    Entity
)
from utca.implementation.predictors.token_searcher.predictor import (
    TokenSearcherPredictor
)
from utca.implementation.tasks.text_processing.clean_text.token_searcher.actions import (
    TokenSearcherTextCleanerPreprocessor,
    TokenSearcherTextCleanerPostprocessor
)

class TokenSearcherTextCleanerInput(IOModel):
    """
    Arguments:
        text (str): Text to clean.
    """
    text: str


class TokenSearcherTextCleanerOutput(NEROutput[Entity]):
    """
    Arguments:
        text (str): Input text.

        cleaned_text (Optional[str], optional): Cleaned text. Equals to None, 
            if clean was set to False.
    """
    text: str
    cleaned_text: Optional[str] = None


class TokenSearcherTextCleaner(
    NERTask[Input, NEROutputType]
):
    """
    Task for text cleaning
    """
    def __init__(
        self,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[Component]=None,
        postprocess: Optional[Component]=None,
        input_class: Type[Input]=TokenSearcherTextCleanerInput,
        output_class: Type[NEROutputType]=TokenSearcherTextCleanerOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            predictor (Optional[Predictor[Any, Any]], optional): Predictor that will be used in task. 
                If equals to None, default TokenSearcherPredictor will be used. 
                Defaults to None.

            preprocess (Optional[Component], optional): Component executed 
                before predictor. If equals to None, default component will be used. 
                Defaults to None.

                Default component:
                    TokenSeatcherTextCleanerPreprocessor
            
            postprocess (Optional[Component], optional): Component executed
                after predictor. If equals to None, default component will be used.
                Defaults to None.

                Default component:
                    TokenSearcherTextCleanerPostprocessor
            
            input_class (Type[Input], optional): Class for input validation. 
                Defaults to TokenSearcherTextCleanerInput.

            output_class (Type[NEROutputType], optional): Class for output validation. 
                Defaults to TokenSearcherTextCleanerOutput.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(
            predictor=predictor or TokenSearcherPredictor(),
            preprocess=preprocess or TokenSearcherTextCleanerPreprocessor(),
            postprocess=postprocess or TokenSearcherTextCleanerPostprocessor(),
            input_class=input_class,
            output_class=output_class,
            name=name,
        )