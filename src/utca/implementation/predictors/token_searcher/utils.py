from typing import Any, Dict, Union, Optional, overload
import string

from utca.core.task_level_3.objects.objects import (
    Entity, ClassifiedEntity
)

def clean_span(text: str, start: int, end: int, shift: int=0):
    junk = {*string.punctuation, *' \n\r\t'}
    
    start += shift
    end += shift
    while start != end - 1 and text[start] in junk:
        start += 1
    while end != start and text[end - 1] in string.punctuation:
        end -= 1
    return text[start:end], start, end


@overload
def build_entity(
    text: str, 
    raw_entity: Dict[str, Any], 
    threshold: float, 
    label: None=None,
    shift: int=0
) -> Union[Entity, None]:
    ...


@overload
def build_entity(
    text: str, 
    raw_entity: Dict[str, Any], 
    threshold: float, 
    label: str,
    shift: int=0
) -> Union[ClassifiedEntity, None]:
    ...


def build_entity(
    text: str,
    raw_entity: Dict[str, Any], 
    threshold: float, 
    label: Optional[str]=None,
    shift: int=0,
) -> Union[Entity, ClassifiedEntity, None]:
    if raw_entity['score'] >= threshold:
        span, start, end = clean_span(
            text, 
            raw_entity['start'] + 1, 
            raw_entity['end'],
            shift
        )
        return ClassifiedEntity(
            start=start,
            end=end,
            span=span,
            score=raw_entity['score'],
            entity=label
        ) if label else Entity(
            start=start,
            end=end,
            span=span,
            score=raw_entity['score'],
        )
    return None