from __future__ import annotations
from abc import ABC
from typing import (
    TypeVar, Any, Dict
)

from pydantic import BaseModel

class Input(BaseModel, ABC):
    def generate_transformable(self):
        return Transformable(self.model_dump())

InputType = TypeVar('InputType', bound=Input, contravariant=True)


# Task №1 - can validate is it right based on input and output class !!!
class Transformable:
    def __init__(self, state: Dict[str, Any]) -> None:
        self.__dict__ = state
    

    def extract(self) -> Dict[str, Any]:
        return self.__dict__
    

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


OutputType = TypeVar('OutputType', bound=Output, contravariant=True)
ConfigType = TypeVar('ConfigType', bound=Config, contravariant=True)