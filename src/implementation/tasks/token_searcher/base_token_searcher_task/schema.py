from typing import TypeVar, Optional, Sequence, Generic, Union

from implementation.models.token_searcher.schema import (
    Input, TokenSearcherModelConfig, EntityType, Output
)
from implementation.models.token_searcher.objects import (
    Entity, ClassifiedEntity
)

class BaseTokenSearcherConfig(TokenSearcherModelConfig):
    threshold: float=0.


BaseTokenSearcherConfigType = TypeVar(
    'BaseTokenSearcherConfigType', bound=BaseTokenSearcherConfig
)


class InputWithThreshold(Input):
    threshold: Optional[float]=None


InputWithThresholdType = TypeVar(
    'InputWithThresholdType', bound=InputWithThreshold
)


class BaseTokenSearcherOutput(Output, Generic[EntityType]):
    output: Sequence[EntityType]


BaseTokenSearcherOutputType = TypeVar(
    'BaseTokenSearcherOutputType', 
    bound=Union[
        BaseTokenSearcherOutput[Entity],
        BaseTokenSearcherOutput[ClassifiedEntity],
    ],
    covariant=True
)