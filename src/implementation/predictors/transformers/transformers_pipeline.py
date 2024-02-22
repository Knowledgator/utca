from typing import TypeVar, Any

from transformers import ( # type: ignore
    pipeline, Pipeline # type: ignore
)

from core.executable_level_1.schema import InputType, OutputType
from core.predictor_level_2.predictor import Predictor
from core.executable_level_1.schema import Config

class TransformersPipelineConfig(Config):    
    def __init__(self, **kwargs: Any):
        self.pipeline: Pipeline = pipeline(**kwargs) # type: ignore


    def __setattr__(self, name: str, value: Any) -> None: # disable pydantic
        self.__dict__[name] = value


TransformersPipelineConfigType = TypeVar(
    'TransformersPipelineConfigType', 
    bound=TransformersPipelineConfig, 
    contravariant=True
)

class TransformersPipeline(
    Predictor[
        TransformersPipelineConfigType, 
        InputType, 
        OutputType
    ]
):  
    def __init__(self, cfg: TransformersPipelineConfigType) -> None:        
        self.pipeline = cfg.pipeline 
        super().__init__(cfg)


    def get_predictions(self, inputs: Any) -> Any:
        return self.pipeline(inputs) # type: ignore