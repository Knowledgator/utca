from pydantic import BaseModel

class Entity(BaseModel):
    start: int
    end: int
    span: str
    score: float


class ClassifiedEntity(Entity):
    entity: str