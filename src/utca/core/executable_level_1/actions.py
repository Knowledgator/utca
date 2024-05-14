from __future__ import annotations
from abc import abstractmethod
from typing import (
    Any, Dict, List, Callable, Optional, TypeVar, Generic, 
    TYPE_CHECKING, cast
)
import logging
import copy

from utca.core.exceptions import InvalidQuery, InputDataKeyError, IvalidInputData
from utca.core.executable_level_1.schema import Transformable, ReplacingScope
from utca.core.executable_level_1.component import Component
from utca.core.executable_level_1.interpreter import Evaluator
from utca.core.exceptions import ActionError
if TYPE_CHECKING:
    from utca.core.executable_level_1.executor import ActionExecutor


ActionInput = TypeVar("ActionInput")
"""
Type variable for action input
"""
ActionOutput = TypeVar("ActionOutput")
"""
Type variable for action output
"""

class Action(Generic[ActionInput, ActionOutput], Component):
    """
    Base action class
    """
    def __init__(
        self, 
        name: Optional[str]=None,
        default_key: str="output",
        replace: ReplacingScope=ReplacingScope.INPLACE,
    ):
        """
        Args:
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
            
            default_key (str, optional): Default key used for results that is not of type Dict.
                Defaults to "output".
            
            replace (ReplacingScope, optional): Replacing strategy. Defaults to ReplacingScope.INPLACE.
        """
        super().__init__(name)
        self.default_key = default_key
        self.replace = replace


    def __call__(
        self, 
        input_data: Transformable,
        evaluator: Optional[Evaluator]=None,
    ) -> Transformable:
        """
        Action Call

        Args:
            input_data (Transformable): Data that is used in action.
            
            evaluator (Optional[Evaluator], optional): Evaluator in context of which action executed.
                If equals to None, default evaluator will be created. Defaults to None.
        Raises:
            ActionError: Raised if action was executed unsuccessfully

        Returns:
            Transformable: Result of executed action.

        Notes:
            If result of Action.execute is None, will return input_data.

            If result of Action.execute is not of type Dict, result will be seted
                to default_key(By default equals to "output").
        """
        if not evaluator:
            evaluator = self.set_up_default_evaluator()

        data = input_data.__dict__
        try:
            result = self.execute(copy.copy(cast(ActionInput, data)))
        except Exception as e:
            raise ActionError(self.name, e)
        
        evaluator.log(logging.DEBUG, f"Action: {self.name}: Executed")

        if result is None:
            return input_data

        if isinstance(result, Dict):
            if self.replace in (ReplacingScope.GLOBAL, ReplacingScope.LOCAL):
                return Transformable(cast(Dict[str, Any], result))
            input_data.update(cast(Dict[str, Any], result))
            return input_data

        if self.replace == ReplacingScope.GLOBAL:
            return Transformable({
                self.default_key: result
            })
        setattr(
            input_data,
            self.default_key,
            result,
        )
        return input_data


    def use(
        self,
        get_key: Optional[str]=None,
        set_key: Optional[str]=None,
        default_key: Optional[str]=None,
        replace: Optional[ReplacingScope]=None,
    ) -> ActionExecutor:
        """
        Creates ActionExecutor which manages context

        Args:
            get_key (Optional[str], optional): Which key value of input_data will be used. 
                If value equal to None, root dict will be used. Defaults to None.

           set_key (Optional[str], optional): Which key will be used to set result value. 
                If set_key value equal to None:
                    - if result of type Dict[str, Any], update root dict;
                    - else, set result to default_key.
                Defaults to None.

            default_key (Optional[str], optional): Default key used for results that is not of type Dict.
                If equals to None, this action default_key will be used. Defaults to None.

            replace (Optional[ReplacingScope], optional): Replacing strategy for executor. 
                If equals to None, this action strategy will be used. Defaults to None.

        Returns:
            ActionExecutor: Wrapper of Action.
        """
        from utca.core.executable_level_1.executor import ActionExecutor
        return ActionExecutor(
            component=self, 
            get_key=get_key, 
            set_key=set_key,
            default_key=default_key or self.default_key,
            replace=replace or self.replace,
        )


    @abstractmethod
    def execute(
        self, 
        input_data: ActionInput,
    ) -> ActionOutput:
        """
        Main logic of action

        Args:
            input_data (ActionInput): Data that will be used.

        Returns:
            ActionOutput: Data that will be returned.
        """
        ...


class Flush(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Remove specific keys or all
    """
    def __init__(
        self, 
        keys: Optional[List[str]]=None,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            keys (Optional[List[str]], optional): Keys for removing. 
                If equals to None, all keys will be removed. Defaults to None.

            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name, replace=ReplacingScope.LOCAL)
        self.keys = keys


    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Remove specified keys

        Args:
            input_data (Dict[str, Any]): Current data.

        Raises:
            InputDataKeyError: Key for removing doesn't exist.

        Returns:
            Dict[str, Any]: Updated data.
        """
        if self.keys is None:
            return {}
        for k in self.keys:
            try:
                input_data.pop(k)
            except:
                raise InputDataKeyError(k)
        return input_data


class AddData(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Add provided data to input data
    """
    def __init__(
        self, 
        data: Dict[str, Any],
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            data (Dict[str, Any]): Key/value pairs that will be added to input data.

            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.data = data


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update input data with provided data

        Args:
            input_data (Dict[str, Any]): Current data.

        Returns:
            Dict[str, Any]: Updated data.
        """
        input_data.update(self.data)
        return input_data


class RenameAttribute(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Rename specified key in input data
    """
    def __init__(
        self, 
        old_name: str,
        new_name: str,
        name: Optional[str]=None
    ) -> None:
        """
        Args:
            old_name (str): Current name.

            new_name (str): New name.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name, replace=ReplacingScope.LOCAL)
        self.old_name = old_name
        self.new_name = new_name


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Rename key

        Args:
            input_data (Dict[str, Any]): Current data.

        Raises:
            InputDataKeyError: Key for renaming doesn't exist.

        Returns:
            Dict[str, Any]: Updated data.
        """
        try:
            input_data[self.new_name] = input_data.pop(self.old_name)
        except:
            raise InputDataKeyError(self.old_name)
        return input_data


class RenameAttributeQuery(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Rename attributes keys using query string
    """
    TRANSFORMATION_DELIMITER = ";"
    TRANSFORMATION_POINTER = "<-"
    
    def __init__(
        self, 
        query: str,
        name: Optional[str]=None
    ) -> None:
        """
        Args:
            query (str): Query for renaming.

            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name, replace=ReplacingScope.LOCAL)
        self.query = query


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Rename keys using query

        Args:
            input_data (Dict[str, Any]): Current data.

        Raises:
            InvalidQuery: Provided query is invalid.
            InputDataKeyError: Key for renaming doesn't exist.

        Returns:
            Dict[str, Any]: Updated data.
        """
        transformation_list = self.query.split(
            self.TRANSFORMATION_DELIMITER
        )

        for transf in transformation_list:
            parts = transf.split(self.TRANSFORMATION_POINTER)
            if len(parts) != 2:
                raise InvalidQuery(transf)

            new_name, old_name = [name.strip() for name in parts]

            # Check if the old attribute name exists in the state dictionary
            if old_name not in input_data:
                raise InputDataKeyError(old_name)

            # Set the new name in the state dictionary with the old value
            input_data[new_name] = input_data.pop(old_name)
        return input_data


class SetValue(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Set new value
    """
    def __init__(
        self, 
        key: str,
        value: Any,
        name: Optional[str]=None
    ) -> None:
        """
        Args:
            key (str): Key for which new value will be seted.
            
            value (Any): New value.

            name (Optional[str], optional): name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.key = key
        self.value = value


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Set new value to key

        Args:
            input_data (Dict[str, Any]): Current data.

        Returns:
            Dict[str, Any]: Updated data.
        """
        input_data[self.key] = self.value
        return input_data


class UnpackValue(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Unpack value from nested level
    """
    def __init__(
        self, 
        key: str,
        name: Optional[str]=None
    ) -> None:
        """
        Args:
            key (str): Key to unpack (associated value should be of type Dict[str, Any]).
            
            name (Optional[str], optional): name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name, replace=ReplacingScope.LOCAL)
        self.key = key


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Unpack value of specified key

        Args:
            input_data (Dict[str, Any]): Current data.

        Raises:
            InputDataKeyError: If specified key doesn't exist.
            IvalidInputData: If nested data has invalid type.

        Returns:
            Dict[str, Any]: Updated data.
        """
        try:
            data = input_data.pop(self.key)
        except:
            raise InputDataKeyError(self.key)
        if not isinstance(data, Dict):
            raise IvalidInputData(
                f"Expected: Dict[str, Any]. Recieved value of type: {type(data)}"
            )
        input_data.update(cast(Dict[str, Any], data))
        return input_data
    

class NestToKey(Action[Any, Dict[str, Any]]):
    """
    Nest input data to specified key
    """
    def __init__(
        self, 
        key: str,
        name: Optional[str]=None
    ) -> None:
        """
        Args:
            key (str): Key for nesting.

            name (Optional[str], optional): name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name, replace=ReplacingScope.LOCAL)
        self.key = key


    def execute(self, input_data: Any) -> Dict[str, Any]:
        """
        Nest input data to specified key

        Args:
            input_data (Any): Current data.

        Returns:
            Dict[str, Any]: Updated data.
        """
        return {
            self.key: input_data
        }


class ExecuteFunction(Action[ActionInput, ActionOutput]):
    """
    Execute provided function
    """
    def __init__(
        self, 
        f: Callable[[ActionInput], ActionOutput],
        name: Optional[str]=None,
        default_key: str="output",
        replace: ReplacingScope=ReplacingScope.INPLACE
    ) -> None:
        """
        Args:
            f (Callable[[ActionInput], ActionOutput]): Function for execution.

            name (Optional[str], optional): name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
            
            default_key (str, optional): Default key used for results that is not of type Dict.
                Defaults to "output".

            replace (ReplacingScope, optional): Replacing strategy. Defaults to ReplacingScope.INPLACE.
        """
        super().__init__(
            name or f"{self.__class__.__name__}.{f.__name__}",
            default_key=default_key,
            replace=replace,
        )
        self.f = f


    def execute(self, input_data: ActionInput) -> ActionOutput:
        """
        Execute provided function

        Args:
            input_data (ActionInput): Function input.

        Returns:
            ActionOutput: Function output.
        """
        return self.f(input_data)