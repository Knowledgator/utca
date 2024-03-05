from __future__ import annotations
from abc import ABC
from typing import (
    TypeVar, Any, Dict, Generic, Type, Optional, List, Union,
    TYPE_CHECKING
)

from pydantic import BaseModel, ValidationError

if TYPE_CHECKING:
    from core.executable_level_1.actions import (
        Action, 
        InputState, 
        OutputState,
    )

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
    pos: int = 0

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
        
    
    def update_state(self, action: Action[InputState, OutputState]) -> None:
        from core.executable_level_1.actions import (
            OneToMany, 
            OneToOne,
            ManyToOne
        )
        if isinstance(self.state, Dict):
            if isinstance(action, ManyToOne):
                self.state = action.execute([self.state])
            elif isinstance(action, (OneToOne, OneToMany)):
                self.state = action.execute(self.state)
            else:
                raise ValueError("Invalid Action! Not supported Action Type!")
        else:
            if isinstance(action, ManyToOne):
                self.state = action.execute(self.state)
            elif isinstance(action, OneToOne):
                self.state = [
                    action.execute(s) for s in self.state
                ]
            else:
                raise ValueError("Invalid Action! Not supported Action Type!")

        
    @property
    def is_batch(self):
        return isinstance(self.state, List)
    

    def __next__(self) -> Dict[str, Any]:
        # not thread safe!!!
        if isinstance(self.state, Dict):
            if self.pos == 0:
                self.pos += 1
                return self.state
            raise StopIteration
        
        if self.pos < len(self.state):
            state = self.state[self.pos]
            self.pos += 1
            return state
        raise StopIteration
    

    def __iter__(self) -> Transformable:
        # not thread safe!!!
        self.pos = 0
        return self

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
ConfigType = TypeVar('ConfigType', bound=Config)