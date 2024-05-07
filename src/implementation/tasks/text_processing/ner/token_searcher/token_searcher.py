from typing import Any, List, Optional, Type

from core.executable_level_1.schema import IOModel, Input
from core.executable_level_1.executor import ActionType
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.task import NERTask
from core.task_level_3.schema import (
    NEROutput, NEROutputType
)
from core.task_level_3.objects.objects import (
    ClassifiedEntity
)
from implementation.predictors.token_searcher.predictor import (
    TokenSearcherPredictor
)
from implementation.tasks.text_processing.ner.token_searcher.actions import (
    TokenSearcherNERPreprocessor,
    TokenSearcherNERPostprocessor,
)

class TokenSearcherNERInput(IOModel):
    """
    Arguments:
        text (str): Text to clean.

        labels(List[str]): Labels for classification.
    """
    text: str
    labels: List[str]


class TokenSearcherNEROutput(NEROutput[ClassifiedEntity]):
    """
    Arguments:
        text (str): Input text.

        output (List[ClassifiedEntity]): Classified entities.
    """
    text: str


class TokenSearcherNER(
    NERTask[Input, NEROutputType]
):
    """
    NER task
    """
    def __init__(
        self,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[List[ActionType]]=None,
        postprocess: Optional[List[ActionType]]=None,
        input_class: Type[Input]=TokenSearcherNERInput,
        output_class: Type[NEROutputType]=TokenSearcherNEROutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Arguments:
            predictor (Predictor[Any, Any], optional): Predictor that will be used in task.
                If equals to None, default TokenSearcherPredictor will be used. Defaults to None.
            
            preprocess (Optional[List[Action[Any, Any]]], optional): Chain of actions executed 
                before predictor. If equals to None, default chain will be used. Defaults to None.

                Default chain: 
                    [TokenSearcherNERPreprocessor]
            
            postprocess (Optional[List[Action[Any, Any]]], optional): Chain of actions executed
                after predictor. If equals to None, default chain will be used. Defaults to None.

                Default chain: 
                    [TokenSearcherNERPostprocessor]

            input_class (Type[Input], optional): Class for input validation. Defaults to TokenSearcherNERInput.
            
            output_class (Type[NEROutputType], optional): Class for output validation. Defaults to TokenSearcherNEROutput.
            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        super().__init__(
            predictor=predictor or TokenSearcherPredictor(),
            preprocess=preprocess or [TokenSearcherNERPreprocessor()],
            postprocess=postprocess or [TokenSearcherNERPostprocessor()],
            input_class=input_class,
            output_class=output_class,
            name=name,
        )