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
from utca.implementation.predictors.gliner_predictor.predictor import (
    GLiNERPredictor, GLiNERPredictorConfig
)
from utca.implementation.tasks.text_processing.textual_q_and_a.gliner_task.actions import (
    GLiNERQandAPreprocessor,
    GLiNERQandAPostprocessor
)

class GLiNERQandAInput(IOModel):
    """
    Arguments:
        text (str): Text to use.

        question (str): Question to answer.
    """
    text: str
    question: str


class GLiNERQandAOutput(NEROutput[Entity]):
    """
    Arguments:
        text (str): Input text.

        question (str): Answered question.
        
        output (List[Entity]): Answers.
    """
    text: str
    question: str


class GLiNERQandA(
    NERTask[Input, NEROutputType]
):
    """
    Textual Q&A task
    """
    default_model: str = "knowledgator/gliner-multitask-large-v0.5"

    def __init__(
        self,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[Component]=None,
        postprocess: Optional[Component]=None,
        input_class: Type[Input]=GLiNERQandAInput,
        output_class: Type[NEROutputType]=GLiNERQandAOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            predictor (Optional[Predictor[Any, Any]], optional): Predictor that will be used in task. 
                If equals to None, default predictor will be used. Defaults to None.
            
            preprocess (Optional[Component], optional): Component executed
                before predictor. If equals to None, default component will be used. Defaults to None.

                Default component: 
                    GLiNERQandAPreprocessor
            
            postprocess (Optional[Component], optional): Component executed
                after predictor. If equals to None, default component will be used. Defaults to None.

                Default component: 
                    GLiNERQandAPostprocessor
            
            input_class (Type[Input], optional): Class for input validation. 
                Defaults to GLiNERQandAInput.
            
            output_class (Type[NEROutputType], optional): Class for output validation.
                Defaults to GLiNERQandAOutput.
            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        super().__init__(
            predictor=predictor or GLiNERPredictor(GLiNERPredictorConfig(model_name=self.default_model)),
            preprocess=preprocess or GLiNERQandAPreprocessor(),
            postprocess=postprocess or GLiNERQandAPostprocessor(),
            input_class=input_class,
            output_class=output_class,
            name=name,
        )