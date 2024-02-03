from hmac import new
import string
from typing import Any, Dict, Generic, Type

from pydantic import  ValidationError

from core.executable_level_1.schema import InputType


TRANSFORMATION_DELIMITER = ";"
TRANSFORMATION_POINTER = "<-"

class Validator(Generic[InputType]):
    def __init__(self, input_validation: Type[InputType]) -> None:
        self.input_validation = input_validation

    def validate(self, toValidate: Dict[str, Any]) -> InputType:
        return self.input_validation(**toValidate)


class Transformable():
    state:  Dict[str, Any]
    def __init__(self, input: Dict[str, Any]) -> None:
        self.state = input
    def __setattr__(self, __name: str, __value: Any) -> None:
        self.__dict__[__name] = __value
    def merge_state(self, input: Dict[str, Any], new_priority: bool):
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
    def rename_state_attr(self, query: str):
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


class AddData():
    data: Dict[str, Any]
    def __init__(self,  data: Dict[str, Any]) -> None:
        self.data = data

class RenameAttribute():
    old_name: str
    new_name: str
    def __init__(self, old_name: str, new_name: str) -> None:
        self.old_name = old_name
        self.new_name = new_name
        

class MergeData():
    def __init__(self, data: Dict[str, Any], new_priority: bool) -> None:
        self.data = data
        self.new_priority = new_priority

class ChangeValue():
    def __init__(self, key: str, value: Any) -> None:
        self.key = key
        self.value = value

# for pipeline     
# class Data 
# class Alter


# input | model(transform) + Data(dict) + Alter("query") | model | db