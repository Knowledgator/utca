from typing import Any, List, Optional, Type

from utca.core.executable_level_1.component import Component
from utca.core.executable_level_1.schema import IOModel, Input
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
        text (str): Text to process.

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
        preprocess: Optional[Component]=None,
        postprocess: Optional[Component]=None,
        input_class: Type[Input]=GLiNERInput,
        output_class: Type[NEROutputType]=GLiNEROutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Arguments:
            predictor (Optional[Predictor[Any, Any]], optional): Predictor that will be used in task.
                If equals to None, default GLiNERPredictor will be used. Defaults to None.
            
            preprocess (Optional[Component], optional): Component executed 
                before predictor. If equals to None, default component will be used. Defaults to None.

                Default component: 
                    GLiNERPreprocessor
            
            postprocess (Optional[Component], optional): Component executed
                after predictor. If equals to None, default component will be used. Defaults to None.

                Default component: 
                    GLiNERPostprocessor

            input_class (Type[Input], optional): Class for input validation. Defaults to GLiNERInput.
            
            output_class (Type[NEROutputType], optional): Class for output validation. Defaults to GLiNEROutput.
            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        super().__init__(
            predictor=predictor or GLiNERPredictor(),
            preprocess=preprocess or GLiNERPreprocessor(),
            postprocess=postprocess or GLiNERPostprocessor(),
            input_class=input_class,
            output_class=output_class,
            name=name,
        )