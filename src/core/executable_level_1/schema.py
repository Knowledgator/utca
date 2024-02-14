from abc import ABC, abstractmethod
from typing import  Callable, TypeVar, Any, Dict, Generic, Type

from pydantic import BaseModel, ValidationError

from core.executable_level_1.component import Component
from core.executable_level_1.statements_types import ACTION, STATEMENT_TYPE, Statement




class Input(BaseModel, ABC):
    ...

InputType = TypeVar('InputType', bound=Input)



class Action(Component, ABC):
    @abstractmethod
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        ...
    def generate_statement(self) -> Dict[str, Any]:
        return {STATEMENT_TYPE: Statement.ACTION_STATEMENT, ACTION: self}





class AddData(Action):
    data: Dict[str, Any]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data


    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        state.update(self.data)
        return state


class RenameAttribute(Action):
    old_name: str
    new_name: str

    def __init__(self, old_name: str, new_name: str) -> None:
        self.old_name = old_name
        self.new_name = new_name


    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        state[self.new_name] = state.pop(self.old_name)
        return state


class ChangeValue(Action):
    key: str
    value: Any

    def __init__(self, key: str, value: Any) -> None:
        self.key = key
        self.value = value


    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        state[self.key] = self.value
        return state


class RenameAttributeQuery(Action):
    TRANSFORMATION_DELIMITER = ";"
    TRANSFORMATION_POINTER = "<-"
    
    query: str

    def __init__(self, query: str) -> None:
        self.query = query

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Return the new name."""
        transformation_list = self.query.split(
            self.TRANSFORMATION_DELIMITER
        )

        for transf in transformation_list:
            parts = transf.split(self.TRANSFORMATION_POINTER)
            if len(parts) != 2:
                raise ValueError(f"Invalid transformation format: '{transf}'")

            new_name, old_name = [name.strip() for name in parts]

            # Check if the old attribute name exists in the state dictionary
            if old_name not in state:
                raise KeyError(f"Attribute '{old_name}' not found in state.")

            # Set the new name in the state dictionary with the old value
            state[new_name] = state.pop(old_name)
        return state


class MergeData(Action):
    data: Dict[str, Any]
    new_priority: bool

    def __init__(self, data: Dict[str, Any], new_priority: bool = True) -> None:
        self.data = data
        self.new_priority = new_priority

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if self.new_priority:
            state = {**state, **self.data}
        else:
            state = {**self.data, **state}
        return state


class ExecuteFunction(Action):
    def __init__(
        self, func: Callable[[Dict[str, Any]], Dict[str, Any]]
    ) -> None:
        self.func = func


    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return self.func(state)


class Validator(Generic[InputType]):
    def __init__(self, input_validation: Type[InputType]) -> None:
        self.input_validation = input_validation

    def validate(self, toValidate: Dict[str, Any]) -> InputType:
        return self.input_validation(**toValidate)


# Task №1 - can validate is it right based on input and output class !!!
class Transformable():
    state: Dict[str, Any]

    def __init__(self, input: Dict[str, Any]) -> None:
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


# input | model(transform) + Data(dict) + Alter("query") | model | db


class Output(BaseModel, ABC):
    def get_transform(self) -> Transformable:
        return Transformable(self.model_dump())
    
    def extract(self) -> Dict[str, Any]:
        return self.model_dump()

    # input -> model -> output -> transfor


class Config(BaseModel, ABC):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"


OutputType = TypeVar('OutputType', bound=Output)
ConfigType = TypeVar('ConfigType', bound=Config, contravariant=True)