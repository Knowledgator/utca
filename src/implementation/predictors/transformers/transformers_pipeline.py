from typing import TypeVar, Any, Type

from transformers import ( # type: ignore
    pipeline, Pipeline # type: ignore
)

from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import (
    PredictorInputType,
    PredictorOutputType,
    PredictorConfig,
    PredictorInput,
    PredictorOutput,
)

class TransformersPipelineConfig(PredictorConfig):    
    def __init__(self, **kwargs: Any):
        self.pipeline: Pipeline = pipeline(**kwargs) # type: ignore


    def __setattr__(self, name: str, value: Any) -> None: # disable pydantic
        self.__dict__[name] = value


TransformersPipelineConfigType = TypeVar(
    'TransformersPipelineConfigType', 
    bound=TransformersPipelineConfig
)

class TransformersPipeline(
    Predictor[
        TransformersPipelineConfigType, 
        PredictorInputType,
        PredictorOutputType
    ]
):  
    def __init__(
        self, 
        cfg: TransformersPipelineConfigType,
        input_class: Type[PredictorInputType]=PredictorInput,
        output_class: Type[PredictorOutputType]=PredictorOutput
    ) -> None:        
        self.pipeline = cfg.pipeline 
        super().__init__(cfg, input_class, output_class)


    def get_predictions(self, **inputs: Any) -> Any:
        return self.pipeline(**inputs) # type: ignore


class SummarizationInput(PredictorInput):
    inputs: Any

SummarizationInputType = TypeVar(
    "SummarizationInputType",
    bound=SummarizationInput
)

class TransformersSummarizationPipeline(
    TransformersPipeline[
        TransformersPipelineConfigType, 
        SummarizationInputType, 
        PredictorOutputType
    ]
):
    def get_predictions(self, **inputs: Any) -> Any:
        return self.pipeline(inputs.pop("inputs"), **inputs) # type: ignore