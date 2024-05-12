from typing import Type, Optional, List, Any

from utca.core.executable_level_1.schema import Input
from utca.core.executable_level_1.executor import ActionType
from utca.core.predictor_level_2.predictor import Predictor
from utca.core.task_level_3.task import NERTask
from utca.core.task_level_3.schema import (
    NEROutput, NEROutputType
)
from utca.core.task_level_3.objects.objects import (
    ClassifiedEntity
)
from utca.implementation.predictors.transformers_predictor.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig
)
from utca.implementation.predictors.transformers_predictor.schema import (
    TransformersBasicInput,
    TransformersBasicOutput
)
from utca.implementation.tasks.text_processing.ner.transformers_ner.actions import (
    TokenClassifierPostprocessor
)

class TransformersTokenClassifierOutput(NEROutput[ClassifiedEntity]):
    ...


class TransformersTokenClassifier(
    NERTask[Input, NEROutputType]
):
    default_model = "dbmdz/bert-large-cased-finetuned-conll03-english"
    
    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[List[ActionType]]=None,
        postprocess: Optional[List[ActionType]]=None,
        input_class: Type[Input]=TransformersBasicInput,
        output_class: Type[NEROutputType]=TransformersTokenClassifierOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            predictor (Predictor[Any, Any], optional): Predictor that will be used in task. 
                If equals to None, default predictor will be used. Defaults to None.

            preprocess (Optional[List[Action[Any, Any]]], optional): Chain of actions executed
                before predictor. Defaults to None.
            
            postprocess (Optional[List[Action[Any, Any]]], optional): Chain of actions executed
                after predictor. If equals to None, default chain will be used. 
                Defaults to None.

                Default chain: 
                    [TokenClassifierPostprocessor]

            input_class (Type[Input], optional): Class for input validation. 
                Defaults to TransformersBasicInput.
            
            output_class (Type[Output], optional): Class for output validation. 
                Defaults to TransformersTokenClassifierOutput.
            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        if not predictor:
            predictor = TransformersPipeline(
                TransformersPipelineConfig(
                    task="token-classification", 
                    model=self.default_model
                ),
                input_class=TransformersBasicInput,
                output_class=TransformersBasicOutput
            )

        super().__init__(
            predictor=predictor,
            preprocess=preprocess or [],
            postprocess=postprocess or [TokenClassifierPostprocessor()],
            input_class=input_class, 
            output_class=output_class,
            name=name,
        )