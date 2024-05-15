from typing import (
    Any, Dict, List, Generic, Optional, TypeVar, cast
)
import copy

from utca.core.executable_level_1.executable import Executable
from utca.core.executable_level_1.actions import Action
from utca.core.executable_level_1.component import Component
from utca.core.executable_level_1.schema import Transformable, ReplacingScope
from utca.core.executable_level_1.interpreter import Evaluator
from utca.core.exceptions import (
    IvalidInputData, 
    ActionError, 
    InputDataKeyError,
    ExecutableError
)

ExecutorComponent = TypeVar("ExecutorComponent", bound=Component)
"""
Type variable for executor wrapped component
"""

class BaseExecutor(Component, Generic[ExecutorComponent]):
    """
    Base executor
    """
    def __init__(
        self, 
        component: ExecutorComponent, 
        get_key: Optional[str]=None,
        set_key: Optional[str]=None,
        default_key: str="output",
        replace: ReplacingScope=ReplacingScope.INPLACE,
    ) -> None:
        """
        Args:
            component (ExecutorComponent): Wrapped component.

            get_key (Optional[str], optional): Which key value of input_data will be used. 
                If value equal to None, root dict will be used. Defaults to None.

            set_key (Optional[str], optional): Which key will be used to set result value. 
                If set_key value equal to None:
                    - if result of type Dict[str, Any], update root dict;
                    - else, set result to default_key.
                Defaults to None.

            default_key (str, optional): Default key used for results that is not of type Dict.
                Defaults to "output".

            replace (ReplacingScope, optional): Replacing strategy for executor.
                Defaults to ReplacingScope.INPLACE.
        """
        self.component = component
        self.get_key = get_key or "__dict__"
        self.set_key = set_key
        self.default_key = default_key
        self.replace = replace
        self._name = self.component.name


    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.__dict__}):"
            f"{self.component.__class__.__name__}: {self.component.name} ({self.component.__dict__})"
        )


class ExecutableExecutor(BaseExecutor[Executable[Any, Any]]):
    def __call__(
        self, 
        input_data: Transformable,
        evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        """
        Args:
            input_data (Transformable): Data that is used in executable.

            evaluator (Optional[Evaluator], optional): Evaluator in context of which executable executed.
                If equals to None, default evaluator will be created. Defaults to None.

        Raises:
            ExecutableError: If any error occures.

        Returns:
            Transformable: Result of execution.
        """
        if not evaluator:
            evaluator = self.set_up_default_evaluator()

        try:
            data = getattr(input_data, self.get_key)
        except:
            raise ExecutableError(
                self.name, InputDataKeyError(self.get_key)
            )
        if isinstance(data, Dict):
            result = self.component.execute(
                copy.copy(cast(Dict[str, Any], data)), evaluator
            )
            if not self.set_key:
                if self.replace in (ReplacingScope.GLOBAL, ReplacingScope.LOCAL):
                    return Transformable(result)
                input_data.update(result)
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
        else:
            raise ExecutableError(self.name, IvalidInputData(
                "Unexpected data type for processing."
            ))

        if self.replace == ReplacingScope.GLOBAL:
            return Transformable({
                self.set_key or self.default_key: result
            })
        setattr(
            input_data,
            self.set_key or self.default_key,
            result
        )
        return input_data
        

class ActionExecutor(BaseExecutor[Action[Any, Any]]):
    def __call__(
        self, 
        input_data: Transformable,
        evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        """
        Args:
            input_data (Transformable): Data that is used in executable.

            evaluator (Optional[Evaluator], optional): Evaluator in context of which action executed.
                If equals to None, default evaluator will be created. Defaults to None.

        Raises:
            ActionError: If any error occur.

        Returns:
            Transformable: Result of execution.
        """
        if not evaluator:
            evaluator = self.set_up_default_evaluator()
        
        try:
            data = getattr(input_data, self.get_key)
        except:
            raise ActionError(
                self.name, InputDataKeyError(self.get_key)
            )

        try:
            result = self.component.execute(copy.copy(data))
        except Exception as e:
            raise ActionError(self.name, e)
        
        if result is None:
            return input_data
        
        if not self.set_key and isinstance(result, Dict):
            if self.replace in (ReplacingScope.GLOBAL, ReplacingScope.LOCAL):
                return Transformable(cast(Dict[str, Any], result))
            input_data.update(cast(Dict[str, Any], result))
            return input_data

        if self.replace == ReplacingScope.GLOBAL:
            return Transformable({
                self.set_key or self.component.default_key: result
            })
        
        setattr(
            input_data,
            self.set_key or self.component.default_key,
            result
        )
        return input_data