from typing import List, TypeVar, Generic, Union

from core.executable_level_1.schema import IOModel
from core.task_level_3.objects.objects import (
    Entity, ClassifiedEntity
)
from core.task_level_3.objects.objects import (
    EntityType
)

class NEROutput(IOModel, Generic[EntityType]):
    """
    Base class for output validation of NER tasks

    Args:
        output (List[EntityType]): List of entities.
    """
    output: List[EntityType]


NEROutputType = TypeVar(
    'NEROutputType', 
    bound=Union[
        NEROutput[Entity],
        NEROutput[ClassifiedEntity],
    ]
)