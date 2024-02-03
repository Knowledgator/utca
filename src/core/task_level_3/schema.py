from typing import TypeVar, Optional, Sequence, Generic, Union

from core.executable_level_1.schema import Input, Output, Config
from core.model_level_2.objects.objects import (
    Entity, ClassifiedEntity
)
from core.model_level_2.objects.objects import (
    EntityType
)

class NERConfig(Config):
    threshold: float=0.


NERConfigType = TypeVar(
    'NERConfigType', bound=NERConfig
)


class InputWithThreshold(Input):
    threshold: Optional[float]=None


InputWithThresholdType = TypeVar(
    'InputWithThresholdType', bound=InputWithThreshold
)


class NEROutput(Output, Generic[EntityType]):
    output: Sequence[EntityType]


BaseTokenSearcherOutputType = TypeVar(
    'BaseTokenSearcherOutputType', 
    bound=Union[
        NEROutput[Entity],
        NEROutput[ClassifiedEntity],
    ]
)