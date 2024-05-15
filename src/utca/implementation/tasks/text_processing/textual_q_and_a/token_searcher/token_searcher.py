from typing import Any, Type, Optional

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
from utca.implementation.tasks.text_processing.textual_q_and_a.token_searcher.actions import (
    TokenSearcherQandAPreprocessor,
    TokenSearcherQandAPostprocessor
)

class TokenSearcherQandAInput(IOModel):
    """
    Arguments:
        text (str): Text to clean.

        question (str): Question to answer.
    """
    text: str
    question: str


class TokenSearcherQandAOutput(NEROutput[Entity]):
    """
    Arguments:
        text (str): Input text.

        question (str): Answered question.
        
        output (List[Entity]): Answers.
    """
    text: str
    question: str


class TokenSearcherQandA(
    NERTask[Input, NEROutputType]
):
    """
    Textual Q&A task
    """
    def __init__(
        self,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[Component]=None,
        postprocess: Optional[Component]=None,
        input_class: Type[Input]=TokenSearcherQandAInput,
        output_class: Type[NEROutputType]=TokenSearcherQandAOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            predictor (Optional[Predictor[Any, Any]], optional): Predictor that will be used in task. 
                If equals to None, default predictor will be used. Defaults to None.
            
            preprocess (Optional[Component], optional): Component executed
                before predictor. If equals to None, default component will be used. Defaults to None.

                Default component: 
                    TokenSearcherQandAPreprocessor
            
            postprocess (Optional[Component], optional): Component executed
                after predictor. If equals to None, default component will be used. Defaults to None.

                Default component: 
                    TokenSearcherQandAPostprocessor
            
            input_class (Type[Input], optional): Class for input validation. 
                Defaults to TokenSearcherQandAInput.
            
            output_class (Type[NEROutputType], optional): Class for output validation.
                Defaults to TokenSearcherQandAOutput.
            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        super().__init__(
            predictor=predictor or TokenSearcherPredictor(),
            preprocess=preprocess or TokenSearcherQandAPreprocessor(),
            postprocess=postprocess or TokenSearcherQandAPostprocessor(),
            input_class=input_class,
            output_class=output_class,
            name=name,
        )