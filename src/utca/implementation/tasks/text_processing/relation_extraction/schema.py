from typing import List, Optional, Tuple

from pydantic import BaseModel

from utca.core.executable_level_1.schema import IOModel
from utca.core.task_level_3.objects.objects import (
    ClassifiedEntity
)

class Relation(BaseModel):
    relation: str
    pairs_filter: Optional[List[Tuple[str, str]]] = None
    distance_threshold: int = -1


class RelationExtractionInput(IOModel):
    """
    Args:
        text (str): Text to process.

        labels(List[str]): Labels for classification.
    """
    text: str
    relations: List[Relation]
    entities: List[ClassifiedEntity]


class Triplet(BaseModel):
    source: ClassifiedEntity
    relation: str
    target: ClassifiedEntity
    score: float


class RelationExtractionOutput(IOModel):
    """
    Args:
        text (str): Input text.

        output (List[ClassifiedEntity]): Classified entities.
    """
    output: List[Triplet]
