from typing import Type, Optional, List, Union

from core.executable_level_1.actions import (
    OneToOne, OneToMany, ManyToOne, ManyToMany
)
from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import (
    PredictorConfig, PredictorInput, PredictorOutput
)
from core.predictor_level_2.schema import (
    PredictorConfig,
    PredictorInput,
    PredictorOutput
)
from core.task_level_3.task import NERTask
from core.task_level_3.schema import (
    InputWithThreshold, 
    NEROutput,
    NERConfig 
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


class ModelInput(PredictorInput):
    inputs: str


class TokenClassifierTask(
    NERTask[
        NERConfig,
        TokenClassifierInput, 
        NEROutput[ClassifiedEntity],
    ]
):
    default_model = "dbmdz/bert-large-cased-finetuned-conll03-english"
    
    def __init__(
        self,
        *,
        cfg: Optional[NERConfig]=None, 
        predictor: Optional[Predictor[
            PredictorConfig, 
            PredictorInput, 
            PredictorOutput
        ]]=None,
        preprocess: Optional[List[Union[OneToOne, OneToMany, ManyToOne, ManyToMany]]]=None,
        postprocess: Optional[List[Union[OneToOne, OneToMany, ManyToOne, ManyToMany]]]=None,
        input_class: Type[TokenClassifierInput]=TokenClassifierInput,
        output_class: Type[NEROutput[ClassifiedEntity]]=NEROutput[ClassifiedEntity]
    ) -> None:

        if not predictor:
            predictor = TransformersPipeline(
                TransformersPipelineConfig(
                    task="token-classification", 
                    model=self.default_model
                ),
                input_class=ModelInput
            )

        super().__init__(
            cfg=cfg or NERConfig(), 
            predictor=predictor,
            preprocess=preprocess or [],
            postprocess=postprocess or [TokenClassifierPostprocessor()],
            input_class=input_class, 
            output_class=output_class,
        )