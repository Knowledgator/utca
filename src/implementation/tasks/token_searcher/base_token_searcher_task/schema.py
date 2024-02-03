from typing import TypeVar, Optional, Sequence, Generic, Union

from core.executable_level_1.schema import Input, Output, Config
from implementation.models.objects.objects import (
    Entity, ClassifiedEntity
)
from implementation.models.objects.schema import (
    EntityType
)

class BaseTokenSearcherConfig(Config):
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
    ]
)