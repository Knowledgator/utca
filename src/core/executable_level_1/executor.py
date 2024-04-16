from typing import (
    Any, Dict, List, Generic, Optional, TypeVar, cast
)

from core.executable_level_1.executable import Executable
from core.executable_level_1.actions import Action
from core.executable_level_1.component import Component
from core.executable_level_1.schema import Transformable
from core.executable_level_1.exceptions import IvalidInputDataValue, ActionError
from core.executable_level_1.interpreter import Evaluator

ExecutorComponent = TypeVar("ExecutorComponent", Executable[Any, Any], Action[Any, Any])

class BasicExecutor(Component, Generic[ExecutorComponent]):
    def __init__(
        self, 
        component: ExecutorComponent, 
        get_key: Optional[str]=None,
        set_key: Optional[str]=None
    ) -> None:
        self.component = component
        self.get_key = get_key or "__dict__"
        self.set_key = set_key
    

    @property
    def name(self) -> str:
        return self.component.name


    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.__dict__}):"
            f"{self.component.__class__.__name__}: {self.component.name} ({self.component.__dict__})"
        )


class ExecutableExecutor(BasicExecutor[Executable[Any, Any]]):
    def __call__(
        self, 
        input_data: Transformable,
        evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        if not evaluator:
            evaluator = self.set_up_default_evaluator()

        data = getattr(input_data, self.get_key)
        if isinstance(input_data, Dict):
            result = self.component.execute(
                cast(Dict[str, Any], data), evaluator
            )
            if not self.set_key:
                input_data.update(result)
            else:
                setattr(
                    input_data, 
                    self.set_key,
                    result
                )
            return input_data
        elif isinstance(data, List):
            result = [
                {
                    **i,
                    **self.component.execute(
                        i, evaluator
                    )
                }
                for i in cast(List[Dict[str, Any]], data)
            ]
            setattr(
                input_data,
                self.set_key or self.component.default_key,
                result
            )
            return input_data
        else:
            raise IvalidInputDataValue()
        

class ActionExecutor(BasicExecutor[Action[Any, Any]]):
    def __call__(
        self, 
        input_data: Transformable,
        evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        if not evaluator:
            evaluator = self.set_up_default_evaluator()
        
        data = getattr(input_data, self.get_key)
        
        try:
            result = self.component.execute(data)
        except Exception as e:
            raise ActionError(self.name, e)
        
        if result is None:
            return input_data
        
        if not self.set_key and isinstance(result, Dict):
            input_data.update(cast(Dict[str, Any], result))
            return input_data

        setattr(
            input_data,
            self.set_key or self.component.default_key,
            result
        )
        return input_data