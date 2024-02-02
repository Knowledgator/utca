from abc import ABC
from typing import  TypeVar

from pydantic import BaseModel

from core.executable_level_1.transformable import Transformable


InputType = TypeVar('InputType', bound='Input')
OutputType = TypeVar('OutputType', bound='Output')

class Input(BaseModel, ABC):
    pass



class Output(BaseModel,  ABC):
    def get_transform(self):
        return Transformable(self.model_dump())
    def extract(self):
        return self.model_dump()


# input -> model -> output -> transfor