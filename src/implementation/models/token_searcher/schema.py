from typing import TypeVar, Dict, Any

from core.model_level_2.schema import Config
from core.executable_level_1.schema import Input, Output
from implementation.models.token_searcher.objects import (
    Entity
)

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