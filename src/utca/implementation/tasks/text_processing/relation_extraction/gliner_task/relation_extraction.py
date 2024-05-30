from typing import Any, Optional, Type

from utca.core.executable_level_1.component import Component
from utca.core.executable_level_1.schema import Input, Output
from utca.core.predictor_level_2.predictor import Predictor
from utca.core.task_level_3.task import Task
from utca.implementation.predictors.gliner_predictor.predictor import (
    GLiNERPredictor, GLiNERPredictorConfig
)
from utca.implementation.tasks.text_processing.ner.gliner_task.actions import (
    GLiNERPreprocessor,
)
from utca.implementation.tasks.text_processing.relation_extraction.schema import (
    RelationExtractionInput, RelationExtractionOutput
)
from utca.implementation.tasks.text_processing.relation_extraction.gliner_task.actions import (
    GLiNERRelationExtractionPreprocessor,
    GLiNERRelationExtractionPostprocessor,
)

class GLiNERRelationExtraction(Task[Input, Output]):
    """
    Relation extraction task
    """
    default_model: str = "knowledgator/gliner-multitask-large-v0.5"

    def __init__(
        self,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[Component]=None,
        postprocess: Optional[Component]=None,
        input_class: Type[Input]=RelationExtractionInput,
        output_class: Type[Output]=RelationExtractionOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Arguments:
            predictor (Optional[Predictor[Any, Any]], optional): Predictor that will be used in task.
                If equals to None, GLiNERPredictor with "knowledgator/gliner-multitask-large-v0.5" model
                will be used. Defaults to None.
            
            preprocess (Optional[Component], optional): Component executed 
                before predictor. If equals to None, default component will be used. Defaults to None.

                Default component: 
                    GLiNERPreprocessor | GLiNERRelationExtractionPreprocessor
            
            postprocess (Optional[Component], optional): Component executed
                after predictor. If equals to None, default component will be used. Defaults to None.

                Default component: 
                    GLiNERRelationExtractionPostprocessor

            input_class (Type[Input], optional): Class for input validation. Defaults to RelationExtractionInput.
            
            output_class (Type[Output], optional): Class for output validation. Defaults to RelationExtractionOutput.
            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        super().__init__(
            predictor=predictor or GLiNERPredictor(GLiNERPredictorConfig(model_name=self.default_model)),
            preprocess=preprocess or (
                GLiNERPreprocessor() | GLiNERRelationExtractionPreprocessor()
            ),
            postprocess=postprocess or GLiNERRelationExtractionPostprocessor(),
            input_class=input_class,
            output_class=output_class,
            name=name,
        )