from abc import ABC
from typing import TypeVar

from pydantic import BaseModel

InputType = TypeVar('InputType', bound='Input')
OutputType = TypeVar('OutputType', bound='Output')

class Input(BaseModel, ABC):
    pass

class Output(BaseModel, ABC):
    pass