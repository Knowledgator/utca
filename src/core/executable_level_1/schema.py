from __future__ import annotations
from abc import ABC
from typing import (
    Optional, TypeVar, Any, Dict
)
from enum import Enum

from pydantic import BaseModel

class Input(BaseModel, ABC):
    def generate_transformable(self):
        return Transformable(self.model_dump())


# Task №1 - can validate is it right based on input and output class !!!
class Transformable:
    def __init__(self, state: Optional[Dict[str, Any]]=None) -> None:
        self.__dict__ = state or {}
    

    def extract(self) -> Dict[str, Any]:
        return self.__dict__
    

    def update(self, data: Dict[str, Any]) -> None:
        self.__dict__.update(data)

    
    def flush(self) -> None:
        self.__dict__ = {}


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"


class Output(BaseModel, ABC):
    def get_transform(self) -> Transformable:
        return Transformable(self.model_dump())
    
    def extract(self) -> Dict[str, Any]:
        return self.model_dump()

    # input -> model -> output -> transfor


class Config(BaseModel, ABC):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"


InputType = TypeVar('InputType', bound=Input)
OutputType = TypeVar('OutputType', bound=Output)


class ReplacingScope(Enum):
    INPLACE = 0
    GLOBAL = 1
    LOCAL = 2