from __future__ import annotations
from abc import ABC
from typing import (
    TypeVar, Any, Dict, Generic, Type, Optional, List, Union,
    TYPE_CHECKING
)

from pydantic import BaseModel, ValidationError

if TYPE_CHECKING:
    from core.executable_level_1.actions import Action

class Input(BaseModel, ABC):
    def generate_transformable(self):
        return Transformable(self.model_dump())

InputType = TypeVar('InputType', bound=Input)


class Validator(Generic[InputType]):
    def __init__(self, input_validation: Type[InputType]) -> None:
        self.input_validation = input_validation


    def validate(self, toValidate: Dict[str, Any]) -> InputType:
        return self.input_validation(**toValidate)


# Task №1 - can validate is it right based on input and output class !!!
class Transformable():
    state: Union[Dict[str, Any], List[Dict[str, Any]]]

    def __init__(self, input: Union[Dict[str, Any], List[Dict[str, Any]]]) -> None:
        self.state = input

    
    def __setattr__(self, __name: str, __value: Any) -> None:
        self.__dict__[__name] = __value
    

    def extract(self):
        return self.state
    

    # for finding particular unmatched fields
    def incomplete_field(self):
        pass
    
    
    def validate(self, validator: Validator[InputType]):
        try:
            validator.validate(self.state)
            return True
        except ValidationError as e:
             print(e.errors())
             return False
        
    
    def update_state(self, action: Action) -> None:
        self.state = action.execute(self.state)

        
    @property
    def is_batch(self):
        return isinstance(self.state, List)

# input | model(transform) + Data(dict) + Alter("query") | model | db


class Output(BaseModel, ABC):
    def get_transform(self) -> Transformable:
        return Transformable(self.model_dump())
    
    def extract(self) -> Dict[str, Any]:
        return self.model_dump()

    # input -> model -> output -> transfor


class Config(BaseModel, ABC):
    max_workers: int = 1
    timeout: Optional[float] = None 

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"


OutputType = TypeVar('OutputType', bound=Output)
ConfigType = TypeVar('ConfigType', bound=Config, contravariant=True)
State = TypeVar("State", Dict[str, Any], List[Dict[str, Any]])