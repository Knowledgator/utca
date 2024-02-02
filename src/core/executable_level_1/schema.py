from abc import ABC
from typing import  TypeVar, Any, Dict

from pydantic import BaseModel

# from core.executable_level_1.transformable import Transformable


class Input(BaseModel, ABC):
    ...


class Output(BaseModel, ABC):
    ...
    # def get_transform(self) -> Transformable:
    #     return Transformable(self.model_dump())
    
    # def extract(self) -> Dict[str, Any]:
    #     return self.model_dump()

    # input -> model -> output -> transfor


InputType = TypeVar('InputType', bound=Input)
OutputType = TypeVar('OutputType', bound=Output)