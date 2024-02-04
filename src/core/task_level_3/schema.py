from typing import TypeVar, Optional, Sequence, Generic, Union

from core.executable_level_1.schema import Input, Output, Config
from core.task_level_3.objects.objects import (
    Entity, ClassifiedEntity
)
from core.task_level_3.objects.objects import (
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


NEROutputType = TypeVar(
    'NEROutputType', 
    bound=Union[
        NEROutput[Entity],
        NEROutput[ClassifiedEntity],
    ]
)