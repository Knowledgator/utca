from __future__ import annotations
from abc import ABC, abstractmethod
from typing import (
    Tuple, Callable, TypeVar, Any, Dict, Generic, Type, Optional, cast,
    List, Union
)

from pydantic import BaseModel, ValidationError
from PIL import Image, ImageOps

from core.executable_level_1.component import Component
from core.executable_level_1.statements_types import Statement

class Input(BaseModel, ABC):
    def generate_transformable(self):
        return Transformable(self.model_dump())

InputType = TypeVar('InputType', bound=Input)


class Action(Component):
    def generate_statement(self) -> Dict[str, Any]:
        return {"type": Statement.ACTION_STATEMENT,  Statement.ACTION_STATEMENT.value: self}
    @abstractmethod
    def execute(self, input_data: Any) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        pass


class AddData(Action):
    data: Dict[str, Any]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data.update(self.data)
        return input_data


class RenameAttribute(Action):
    old_name: str
    new_name: str

    def __init__(self, old_name: str, new_name: str) -> None:
        self.old_name = old_name
        self.new_name = new_name


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data[self.new_name] = input_data.pop(self.old_name)
        return input_data


class ChangeValue(Action):
    key: str
    value: Any

    def __init__(self, key: str, value: Any) -> None:
        self.key = key
        self.value = value


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data[self.key] = self.value
        return input_data


class RenameAttributeQuery(Action):
    TRANSFORMATION_DELIMITER = ";"
    TRANSFORMATION_POINTER = "<-"
    
    query: str

    def __init__(self, query: str) -> None:
        self.query = query

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
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
            if old_name not in input_data:
                raise KeyError(f"Attribute '{old_name}' not found in state.")

            # Set the new name in the state dictionary with the old value
            input_data[new_name] = input_data.pop(old_name)
        return input_data


class MergeData(Action):
    data: Dict[str, Any]
    new_priority: bool

    def __init__(self, data: Dict[str, Any], new_priority: bool = True) -> None:
        self.data = data
        self.new_priority = new_priority

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if self.new_priority:
            state = {**input_data, **self.data}
        else:
            state = {**self.data, **input_data}
        return state


class ExecuteFunction(Action):
    def __init__(
        self, func: Callable[[Dict[str, Any]], Union[Dict[str, Any], List[Dict[str, Any]]]]
    ) -> None:
        self.func = func


    def execute(self, input_data: Dict[str, Any]) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        return self.func(input_data)


class ImageAction(Action): # TODO: add more and revisit structure
    ...


class RotateImage(ImageAction):
    def __init__(self, rotation: float) -> None:
        self.rotation = rotation


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data['image'] = cast(
            Image.Image, input_data['image']
        ).rotate(self.rotation)
        return input_data
    

class ResizeImage(ImageAction):
    def __init__(self, width: int, height: int) -> None:
        self.height = height
        self.width = width


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data['image'] = cast(
            Image.Image, input_data['image']
        ).resize((self.width, self.height))
        return input_data
    

class PadImage(ImageAction):
    def __init__(self, width: int, height: int, color: Optional[str]=None) -> None:
        self.height = height
        self.width = width
        self.color = color


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data['image'] = ImageOps.pad(
            cast(Image.Image, input_data['image']),
            (self.width, self.height),
            color=self.color
        )
        return input_data
    

class CropImage(ImageAction):
    def __init__(self, box: Tuple[int, int, int, int]) -> None:
        self.box = box


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data['image'] = cast(
            Image.Image, input_data['image']
        ).crop(self.box)
        return input_data


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
        if not self.is_batch:
            self.state = action.execute(self.state)
        else:
            self.state = [
                cast(Dict[str, Any], res) for s in self.state
                if (res:=action.execute(s))
            ]

        
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