from typing import List, Optional, Tuple

from pydantic import BaseModel

from utca.core.executable_level_1.schema import IOModel
from utca.core.task_level_3.objects.objects import (
    ClassifiedEntity
)

class Relation(BaseModel):
    """
    Args:
        relation (str): Relation label.

        pairs_filter (Optional[List[Tuple[str, str]]], optional): Expected pairs for relation.
            If equals to None all pairs will be returned. Defaults to None.

        distance_threshold (int, optional): Distance threshold. It specifies the max distance between spans in the text 
            (i.e., the end of the span that is closer to the start of the text and the start of the next one).
            Defaults to -1 (no distance threshold).
    """
    relation: str
    pairs_filter: Optional[List[Tuple[str, str]]] = None
    distance_threshold: int = -1


class RelationExtractionInput(IOModel):
    """
    Args:
        text (str): Text to process.

        relations (List[Relation]): Relations parameters.

        entities (List[ClassifiedEntity]): Entities to use.
    """
    text: str
    relations: List[Relation]
    entities: List[ClassifiedEntity]


class Triplet(BaseModel):
    """
    Args:
        source (ClassifiedEntity): Source entity in the relation.
        
        relation (str): Relation label.
        
        target (ClassifiedEntity): Target entity in the relation.

        score (float): Relation score.
    """
    source: ClassifiedEntity
    relation: str
    target: ClassifiedEntity
    score: float


class RelationExtractionOutput(IOModel):
    """
    Args:
        output (List[Triplet]): Relations triplets.
    """
    output: List[Triplet]
