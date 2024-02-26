from abc import abstractmethod
from typing import (
    Callable, Any, Dict, List, Union, Generic, TypeVar, Type
)

from core.executable_level_1.component import Component
from core.executable_level_1.statements_types import Statement
from core.executable_level_1.schema import State


class Action(Component):    
    @abstractmethod
    def execute(self, input_data: Any) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        pass


    def generate_statement(self) -> Dict[str, Any]:
        return {"type": Statement.ACTION_STATEMENT,  Statement.ACTION_STATEMENT.value: self}

InputState = TypeVar("InputState", Dict[str, Any], List[Dict[str, Any]])
OutputState = TypeVar("OutputState", Dict[str, Any], List[Dict[str, Any]])

class ActionDecorator(Generic[InputState, OutputState]):
    def __init__(
        self, 
        action: Type[Action]
    ) -> None:
        self.action = action


    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.action(*args, **kwargs)


    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return self.action.execute(*args, **kwargs)


class ManyToMany(ActionDecorator[List[Dict[str, Any]], List[Dict[str, Any]]]):
    ...


class OneToOne(ActionDecorator[Dict[str, Any], Dict[str, Any]]):
    ...


class ManyToOne(ActionDecorator[List[Dict[str, Any]], Dict[str, Any]]):
    ...


class OneToMany(ActionDecorator[Dict[str, Any], List[Dict[str, Any]]]):
    ...


@OneToOne
class AddData(Action):
    data: Dict[str, Any]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data.update(self.data)
        return input_data


@OneToOne
class RenameAttribute(Action):
    old_name: str
    new_name: str

    def __init__(self, old_name: str, new_name: str) -> None:
        self.old_name = old_name
        self.new_name = new_name


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data[self.new_name] = input_data.pop(self.old_name)
        return input_data


@OneToOne
class ChangeValue(Action):
    key: str
    value: Any

    def __init__(self, key: str, value: Any) -> None:
        self.key = key
        self.value = value


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data[self.key] = self.value
        return input_data


@OneToOne
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


@OneToOne
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


class ExecuteFunction(Generic[State], Action):
    def __init__(
        self, 
        func: Union[
            Callable[[State], Dict[str, Any]],
            Callable[[State], List[Dict[str, Any]]],
        ]
    ) -> None:
        self.func = func


    def execute(self, input_data: State) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        return self.func(input_data)