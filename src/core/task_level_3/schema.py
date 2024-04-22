from typing import TypeVar, Sequence, Generic, Union

from core.executable_level_1.schema import IOModel
from core.task_level_3.objects.objects import (
    Entity, ClassifiedEntity
)
from core.task_level_3.objects.objects import (
    EntityType
)

class NEROutput(IOModel, Generic[EntityType]):
    output: Sequence[EntityType]


NEROutputType = TypeVar(
    'NEROutputType', 
    bound=Union[
        NEROutput[Entity],
        NEROutput[ClassifiedEntity],
    ]
)