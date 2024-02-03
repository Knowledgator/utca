from typing import TypeVar, Any, Dict

from transformers import ( # type: ignore
    pipeline, Pipeline # type: ignore
)

from core.executable_level_1.schema import Config

class TransformersPipelineConfig(Config):    
    def __init__(self, **kwargs: Dict[str, Any]):
        self.pipeline: Pipeline = pipeline(**kwargs) # type: ignore


    def __setattr__(self, name: str, value: Any) -> None: # disable pydantic
        self.__dict__[name] = value


TransformersPipelineConfigType = TypeVar(
    'TransformersPipelineConfigType', 
    bound=TransformersPipelineConfig, 
    contravariant=True
)