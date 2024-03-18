from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass
from typing import (
    Any, Dict, Callable, Optional, TypeVar, Generic, 
    TYPE_CHECKING, cast
)
import logging

from core.executable_level_1.schema import Transformable
from core.executable_level_1.component import Component
from core.executable_level_1.statements_types import Statement
if TYPE_CHECKING:
    from core.executable_level_1.executor import Executor


ActionInput = TypeVar("ActionInput")
ActionOutput = TypeVar("ActionOutput")

class Action(Generic[ActionInput, ActionOutput], Component):
    default_key: str = "output"

    def __call__(
        self, 
        register: Transformable,
        get_key: Optional[str]=None,
        set_key: Optional[str]=None
    ) -> Transformable:
        input_data = getattr(register, get_key or "__dict__")
        try:
            result = self.execute(input_data)
        except Exception as e:
            raise ValueError(
                f"Action error: {self.__class__}: {e}"
            )
        if result is None:
            return register

        if not isinstance(result, Dict) and not set_key:
            set_key = self.default_key
        setattr(
            register,
            set_key or "__dict__",
            result
        )
        return register

    def use(
        self,
        get_key: Optional[str]=None,
        set_key: Optional[str]=None
    ) -> Executor[Action[Any, Any]]:
        from core.executable_level_1.executor import Executor
        return Executor(
            component=self, 
            get_key=get_key, 
            set_key=set_key
        )


    @property
    def statement(self) -> Statement:
        return Statement.ACTION_STATEMENT


    @abstractmethod
    def execute(
        self, 
        input_data: ActionInput
    ) -> ActionOutput:
        ...


class Log(Action[ActionInput, ActionOutput]):
    def __init__(self, logger: logging.Logger, message: str="") -> None:
        self.logger = logger
        self.message = message


    def execute(self, input_data: ActionInput) -> ActionOutput:
        self.logger.error(self.message)
        self.logger.error(input_data)
        return cast(ActionOutput, input_data)


@dataclass(slots=True)
class AddData(Action[Dict[str, Any], Dict[str, Any]]):
    data: Dict[str, Any]

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            **input_data,
            **self.data
        }


@dataclass(slots=True)
class RenameAttribute(Action[Dict[str, Any], Dict[str, Any]]):
    old_name: str
    new_name: str

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data[self.new_name] = input_data.pop(self.old_name)
        return input_data


@dataclass(slots=True)
class ChangeValue(Action[Dict[str, Any], Dict[str, Any]]):
    key: str
    value: Any

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data[self.key] = self.value
        return input_data


@dataclass(slots=True)
class UnpackValue(Action[Dict[str, Any], Dict[str, Any]]):
    key: str

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data.update(input_data.pop(self.key))
        return input_data 
    

@dataclass(slots=True)
class NestToKey(Action[Dict[str, Any], Dict[str, Any]]):
    key: str

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            self.key: input_data
        }


@dataclass(slots=True)
class RenameAttributeQuery(Action[Dict[str, Any], Dict[str, Any]]):
    TRANSFORMATION_DELIMITER = ";"
    TRANSFORMATION_POINTER = "<-"
    
    query: str

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


@dataclass(slots=True)
class MergeData(Action[Dict[str, Any], Dict[str, Any]]):
    data: Dict[str, Any]
    new_priority: bool

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if self.new_priority:
            return {**input_data, **self.data}
        else:
            return {**self.data, **input_data}


@dataclass(slots=True)
class ExecuteFunction(Action[ActionInput, ActionOutput]):
    f: Callable[[ActionInput], ActionOutput]

    def execute(self, input_data: ActionInput) -> ActionOutput:
        return self.f(input_data)