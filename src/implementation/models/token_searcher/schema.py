from typing import TypeVar, Dict, Any
from abc import ABC

from pydantic import BaseModel

from implementation.models.token_searcher.objects import (
    Entity
)

class Input(BaseModel, ABC):
    pass


class Output(BaseModel, ABC):
    pass


class Config(BaseModel, ABC):
    pass


InputType = TypeVar('InputType', bound=Input)
OutputType = TypeVar('OutputType', bound=Output, covariant=True)
ConfigType = TypeVar('ConfigType', bound=Config, contravariant=True)


class TokenSearcherModelConfig(Config):
    model_name: str
    sents_batch: int=10
    batch_size: int=12
    device: str='cpu'


TokenSearcherModelConfigType = TypeVar(
    'TokenSearcherModelConfigType', 
    bound=TokenSearcherModelConfig, 
    contravariant=True
)

EntityType = TypeVar('EntityType', bound=Entity)


class TokenSearcherModelInput(Input):
    inputs: list[str]


class TokenSearcherModelOutput(Output):
    inputs: list[str]
    output: list[list[Dict[str, Any]]]