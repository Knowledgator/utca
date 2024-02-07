from abc import ABC
from typing import  Callable, TypeVar, Any, Dict, Generic, Type

from pydantic import BaseModel, ValidationError

from core.executable_level_1.component import Component


class Input(BaseModel, ABC):
    ...

InputType = TypeVar('InputType', bound=Input)

TRANSFORMATION_DELIMITER = ";"
TRANSFORMATION_POINTER = "<-"

class Validator(Generic[InputType]):
    def __init__(self, input_validation: Type[InputType]) -> None:
        self.input_validation = input_validation

    def validate(self, toValidate: Dict[str, Any]) -> InputType:
        return self.input_validation(**toValidate)

# Task №1 - can validate is it right based on input and output class !!!
class Transformable(Component):
    state: Dict[str, Any]

    def __init__(self, input: Dict[str, Any]) -> None:
        self.state = input

    
    def __setattr__(self, __name: str, __value: Any) -> None:
        self.__dict__[__name] = __value
    
    
    def merge_state(self, input: Dict[str, Any], new_priority: bool = True):
        if new_priority:
            self.state = {**self.state, **input}
        else:
            self.state = {**input, **self.state}
    
    
    def add_data(self, input: Dict[str, Any]):
        self.state.update(input)


    def change_value(self, key: str, value: Any):
        self.state[key] = value

    """
    Simple language for renaming attributes:
    query = "new_name<-old_name",
    list of transformations are delimited with ';'
    """
    def rename_state_attr_q(self, query: str):
        if not query:
            raise ValueError("No transformation query provided.")

        transformation_list = query.split(TRANSFORMATION_DELIMITER)

        for transf in transformation_list:
            try:
                parts = transf.split("<-")
                if len(parts) != 2:
                    raise ValueError(f"Invalid transformation format: '{transf}'")

                new_name, old_name = [name.strip() for name in parts]

                # Check if the old attribute name exists in the state dictionary
                if old_name not in self.state:
                    raise KeyError(f"Attribute '{old_name}' not found in state.")

                # Get the old value from the state dictionary
                old_value = self.state[old_name]

                # Set the new name in the state dictionary with the old value
                self.state[new_name] = old_value

                # Remove the old name from the state dictionary
                del self.state[old_name]

            except ValueError as ve:
                print(f"Error: {ve}")
            except KeyError as ke:
                print(f"Error: {ke}")
            except Exception as e:
                print(f"Unexpected error: {e}")


    def rename_state_attr(self, old_name: str, new_name: str):
        try:

            # Check if the old attribute name exists in the state dictionary
            if old_name not in self.state:
                raise KeyError(f"Attribute '{old_name}' not found in state.")

            # Get the old value from the state dictionary
            old_value = self.state[old_name]

            # Set the new name in the state dictionary with the old value
            self.state[new_name] = old_value

            # Remove the old name from the state dictionary
            del self.state[old_name]
        except KeyError as ke:
            print(f"Error: {ke}")
        except Exception as e:
            print(f"Unexpected error: {e}")


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


    def custom_tranform(
        self, f: Callable[[Dict[str, Any]], Dict[str, Any]]
    ) -> None:
        self.state = f(self.state)


class Action(Component, ABC):
    pass


class AddData(Action):
    data: Dict[str, Any]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    def get_data(self) -> Dict[str, Any]:
        """Return the data dictionary."""
        return self.data


class RenameAttribute(Action):
    old_name: str
    new_name: str

    def __init__(self, old_name: str, new_name: str) -> None:
        self.old_name = old_name
        self.new_name = new_name

    def get_old_name(self) -> str:
        """Return the old name."""
        return self.old_name

    def get_new_name(self) -> str:
        """Return the new name."""
        return self.new_name

class RenameAttributeQuery(Action):
    query: str

    def __init__(self, query: str) -> None:
        self.query = query

    def get_new_name(self) -> str:
        """Return the new name."""
        return self.query


class MergeData(Action):
    data: Dict[str, Any]
    new_priority: bool

    def __init__(self, data: Dict[str, Any], new_priority: bool = True) -> None:
        self.data = data
        self.new_priority = new_priority

    def get_data(self) -> Dict[str, Any]:
        """Return the data dictionary."""
        return self.data

    def is_new_priority(self) -> bool:
        """Return whether new data has priority."""
        return self.new_priority


class ChangeValue(Action):
    key: str
    value: Any

    def __init__(self, key: str, value: Any) -> None:
        self.key = key
        self.value = value

    def get_key(self) -> str:
        """Return the key."""
        return self.key

    def get_value(self) -> Any:
        """Return the value."""
        return self.value

class ExecuteFunction(Action):
    def __init__(
        self, func: Callable[[Dict[str, Any]], Dict[str, Any]]
    ) -> None:
        self.func = func



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