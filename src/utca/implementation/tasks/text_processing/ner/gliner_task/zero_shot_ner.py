from typing import Any, List, Optional, Type

from utca.core.executable_level_1.schema import IOModel, Input
from utca.core.executable_level_1.executor import ActionType
from utca.core.predictor_level_2.predictor import Predictor
from utca.core.task_level_3.task import NERTask
from utca.core.task_level_3.schema import (
    NEROutput, NEROutputType
)
from utca.core.task_level_3.objects.objects import (
    ClassifiedEntity
)
from utca.implementation.predictors.gliner_predictor.predictor import (
    GLiNERPredictor
)
from utca.implementation.tasks.text_processing.ner.gliner_task.actions import (
    GLiNERPreprocessor,
    GLiNERPostprocessor,
)

class GLiNERInput(IOModel):
    """
    Arguments:
        text (str): Text to clean.

        labels(List[str]): Labels for classification.
    """
    text: str
    labels: List[str]


class GLiNEROutput(NEROutput[ClassifiedEntity]):
    """
    Arguments:
        text (str): Input text.

        output (List[ClassifiedEntity]): Classified entities.
    """
    text: str


class GLiNER(
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
        input_class: Type[Input]=GLiNERInput,
        output_class: Type[NEROutputType]=GLiNEROutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Arguments:
            predictor (Predictor[Any, Any], optional): Predictor that will be used in task.
                If equals to None, default GLiNERPredictor will be used. Defaults to None.
            
            preprocess (Optional[List[Action[Any, Any]]], optional): Chain of actions executed 
                before predictor. If equals to None, default chain will be used. Defaults to None.

                Default chain: 
                    [GLiNERNERPreprocessor]
            
            postprocess (Optional[List[Action[Any, Any]]], optional): Chain of actions executed
                after predictor. If equals to None, default chain will be used. Defaults to None.

                Default chain: 
                    [GLiNERNERPostprocessor]

            input_class (Type[Input], optional): Class for input validation. Defaults to GLiNERNERInput.
            
            output_class (Type[NEROutputType], optional): Class for output validation. Defaults to GLiNERNEROutput.
            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        super().__init__(
            predictor=predictor or GLiNERPredictor(),
            preprocess=preprocess or [GLiNERPreprocessor()],
            postprocess=postprocess or [GLiNERPostprocessor()],
            input_class=input_class,
            output_class=output_class,
            name=name,
        )