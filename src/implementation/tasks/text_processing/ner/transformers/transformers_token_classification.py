from typing import Type, Optional, List, Any

from core.executable_level_1.schema import (
    Input, Output
)
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
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig
)
from implementation.tasks.text_processing.ner.transformers.actions import (
    TokenClassifierPostprocessor
)

class TokenClassifierInput(InputWithThreshold):
    inputs: str


class ModelInput(Input):
    inputs: str


class ModelOutput(Output):
    output: Any


class TokenClassifierTask(
    NERTask[
        TokenClassifierInput, 
        NEROutput[ClassifiedEntity],
    ]
):
    default_model = "dbmdz/bert-large-cased-finetuned-conll03-english"
    
    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Input, Output]]=None,
        preprocess: Optional[List[Action[Any, Any]]]=None,
        postprocess: Optional[List[Action[Any, Any]]]=None,
        input_class: Type[TokenClassifierInput]=TokenClassifierInput,
        output_class: Type[NEROutput[ClassifiedEntity]]=NEROutput[ClassifiedEntity]
    ) -> None:
        if not predictor:
            predictor = TransformersPipeline(
                TransformersPipelineConfig(
                    task="token-classification", 
                    model=self.default_model
                ),
                input_class=ModelInput,
                output_class=ModelOutput
            )

        super().__init__(
            predictor=predictor,
            preprocess=preprocess or [],
            postprocess=postprocess or [TokenClassifierPostprocessor()],
            input_class=input_class, 
            output_class=output_class,
        )