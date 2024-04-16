from __future__ import annotations
from abc import abstractmethod
from typing import (
    Any, Dict, List, Callable, Optional, TypeVar, Generic, 
    TYPE_CHECKING, cast
)
import logging

from core.executable_level_1.schema import Transformable
from core.executable_level_1.component import Component
from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.exceptions import ActionError
if TYPE_CHECKING:
    from core.executable_level_1.executor import ActionExecutor


ActionInput = TypeVar("ActionInput")
ActionOutput = TypeVar("ActionOutput")

class Action(Generic[ActionInput, ActionOutput], Component):
    default_key: str = "output"

    def __call__(
        self, 
        input_data: Transformable,
        evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        if not evaluator:
            evaluator = self.set_up_default_evaluator()

        data = input_data.__dict__
        try:
            result = self.execute(cast(ActionInput, data))
        except Exception as e:
            raise ActionError(self.name, e)
        
        evaluator.log_debug(f"Action: {self.name}: Executed")

        if result is None:
            return input_data

        if isinstance(result, Dict):
            input_data.update(cast(Dict[str, Any], result))
            return input_data
        setattr(
            input_data,
            self.default_key,
            result
        )
        return input_data


    def use(
        self,
        get_key: Optional[str]=None,
        set_key: Optional[str]=None
    ) -> ActionExecutor:
        from core.executable_level_1.executor import ActionExecutor
        return ActionExecutor(
            component=self, 
            get_key=get_key, 
            set_key=set_key
        )


    @abstractmethod
    def execute(
        self, 
        input_data: ActionInput
    ) -> ActionOutput:
        ...


class Flush(Action[Transformable, Transformable]):
    def __init__(
        self, 
        keys: Optional[List[str]]=None,
        name: Optional[str]=None
    ) -> None:
        super().__init__(name)
        self.keys = keys


    def execute(
        self, input_data: Transformable
    ) -> Transformable:
        if self.keys is None:
            input_data.flush()
            return input_data
        for k in self.keys:
            delattr( # possibly dangerous?
                input_data, k
            )
        return input_data
    

    def use(
        self,
        get_key: Optional[str]=None,
        set_key: Optional[str]=None
    ) -> ActionExecutor:
        raise AttributeError("Flush action doesn't support use method!")


    def __call__(
        self, 
        register: Transformable,
        evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        if not evaluator:
            evaluator = self.set_up_default_evaluator()

        try:
            return self.execute(register)
        except Exception as e:
            raise ActionError(self.name, e)


class Log(Action[ActionInput, None]):
    def __init__(
        self, 
        logger: logging.Logger, 
        message: str="",
        open: str="-"*40,
        close: str="-"*40,
        name: Optional[str]=None
    ) -> None:
        super().__init__(name)
        self.logger = logger
        self.message = message
        self.open = open
        self.close = close


    def execute(self, input_data: ActionInput) -> None:
        self.logger.debug(
            "\n".join((
                self.open, 
                self.message, 
                input_data.__repr__(), 
                self.close
            ))
        )


class AddData(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        data: Dict[str, Any],
        name: Optional[str]=None
    ) -> None:
        super().__init__(name)
        self.data = data


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            **input_data,
            **self.data
        }


class RenameAttribute(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        old_name: str,
        new_name: str,
        name: Optional[str]=None
    ) -> None:
        super().__init__(name)
        self.old_name = old_name
        self.new_name = new_name


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data[self.new_name] = input_data.pop(self.old_name)
        return input_data


class ChangeValue(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        key: str,
        value: Any,
        name: Optional[str]=None
    ) -> None:
        super().__init__(name)
        self.key = key
        self.value = value


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data[self.key] = self.value
        return input_data


class UnpackValue(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        key: str,
        name: Optional[str]=None
    ) -> None:
        super().__init__(name)
        self.key = key


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data.update(input_data.pop(self.key))
        return input_data 
    

class NestToKey(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        key: str,
        name: Optional[str]=None
    ) -> None:
        super().__init__(name)
        self.key = key


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            self.key: input_data
        }


class RenameAttributeQuery(Action[Dict[str, Any], Dict[str, Any]]):
    TRANSFORMATION_DELIMITER = ";"
    TRANSFORMATION_POINTER = "<-"
    
    def __init__(
        self, 
        query: str,
        name: Optional[str]=None
    ) -> None:
        super().__init__(name)
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


class MergeData(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        data: Dict[str, Any],
        new_priority: bool=False,
        name: Optional[str]=None
    ) -> None:
        super().__init__(name)
        self.data = data
        self.new_priority = new_priority


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if self.new_priority:
            return {**input_data, **self.data}
        else:
            return {**self.data, **input_data}


class ExecuteFunction(Action[ActionInput, ActionOutput]):
    def __init__(
        self, 
        f: Callable[[ActionInput], ActionOutput],
        name: Optional[str]=None
    ) -> None:
        super().__init__(name or f"{self.__class__.__name__}.{f.__name__}")
        self.f = f


    def execute(self, input_data: ActionInput) -> ActionOutput:
        return self.f(input_data)