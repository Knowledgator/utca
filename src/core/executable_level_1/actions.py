from abc import abstractmethod, ABCMeta
from typing import (
    Callable, Any, Dict, List, Generic, TypeVar
)

from core.executable_level_1.component import Component
from core.executable_level_1.statements_types import Statement

InputState = TypeVar("InputState", Dict[str, Any], List[Dict[str, Any]])
OutputState = TypeVar("OutputState", Dict[str, Any], List[Dict[str, Any]])

class Action(Generic[InputState, OutputState], Component):    
    @abstractmethod
    def execute(self, input_data: InputState) -> OutputState:
        pass


    def generate_statement(self) -> Dict[str, Any]:
        return {"type": Statement.ACTION_STATEMENT,  Statement.ACTION_STATEMENT.value: self}


class ManyToMany(Action[List[Dict[str, Any]], List[Dict[str, Any]]]):
    ...


class OneToOne(Action[Dict[str, Any], Dict[str, Any]]):
    ...


class ManyToOne(Action[List[Dict[str, Any]], Dict[str, Any]]):
    ...


class OneToMany(Action[Dict[str, Any], List[Dict[str, Any]]]):
    ...


class AddData(OneToOne):
    data: Dict[str, Any]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data.update(self.data)
        return input_data


class RenameAttribute(OneToOne):
    old_name: str
    new_name: str

    def __init__(self, old_name: str, new_name: str) -> None:
        self.old_name = old_name
        self.new_name = new_name


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data[self.new_name] = input_data.pop(self.old_name)
        return input_data


class ChangeValue(OneToOne):
    key: str
    value: Any

    def __init__(self, key: str, value: Any) -> None:
        self.key = key
        self.value = value


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data[self.key] = self.value
        return input_data


class RenameAttributeQuery(OneToOne):
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


class MergeData(OneToOne):
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


class DynamicTypeMeta(ABCMeta):
    def __call__(cls, *args: Any, **kwargs: Any):
        if 'type_' in kwargs:
            desired_type = kwargs.pop('type_')
            cls = type(desired_type.__name__, (desired_type,), dict(cls.__dict__))
        instance = cls.__new__(cls, *args, **kwargs)
        cls.__init__(instance, *args, **kwargs)
        return instance


class ExecuteFunction(Action[InputState, OutputState], metaclass=DynamicTypeMeta):
    def __init__(
        self, 
        func: Callable[[InputState], OutputState],
        type_: Action[InputState, OutputState]
    ) -> None:
        self.func = func


    def execute(self, input_data: InputState) -> OutputState:
        return self.func(input_data)


class BatchAdapter(ManyToMany):
    def __init__(self, action: OneToOne):
        self.action = action

    
    def execute(self, input_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [
            self.action.execute(i) for i in input_data
        ]