from __future__ import annotations
from abc import abstractmethod
from typing import (
    Any, Dict, List, Callable, Optional, TypeVar, Generic, 
    TYPE_CHECKING, cast
)
import logging

from core.exceptions import InvalidQuery, InputDataKeyError
from core.executable_level_1.schema import Transformable, ReplacingScope
from core.executable_level_1.component import Component
from core.executable_level_1.interpreter import Evaluator
from core.exceptions import ActionError
if TYPE_CHECKING:
    from core.executable_level_1.executor import ActionExecutor


ActionInput = TypeVar("ActionInput")
ActionOutput = TypeVar("ActionOutput")

class Action(Generic[ActionInput, ActionOutput], Component):
    """
    Basic Action class
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
            
            replace (bool): If true, result will replace old value. Defaults to False.
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
            
            evaluator (Optional[Evaluator], optional): Evaluator in context of wich action executed.
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
            result = self.execute(cast(ActionInput, data))
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
    ) -> ActionExecutor:
        """
        Creates ActionExecutor wich manages get and set keys.

        Args:
            get_key (Optional[str], optional): Which key value of input_data will be used. 
                If value equal to None, root dict will be used. Defaults to None.

            set_key (Optional[str], optional): Which key will be used to set value. 
                If value equal to None:
                    - if value of type Dict[str, Any], update root dict;
                    - else: set value to default_key.
                Defaults to None.

        Returns:
            ActionExecutor: Wrapper of Action.
        """
        from core.executable_level_1.executor import ActionExecutor
        return ActionExecutor(
            component=self, 
            get_key=get_key, 
            set_key=set_key,
            replace=self.replace,
        )


    @abstractmethod
    def execute(
        self, 
        input_data: ActionInput,
    ) -> ActionOutput:
        """
        Custom logic of an action

        Args:
            input_data (ActionInput): Data that will be used.

        Returns:
            ActionOutput: Data that will be returned.
        """
        ...


class Flush(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Remove specific keys or all.
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
        Args:
            input_data (Transformable): Data to process.

        Returns:
            Transformable: Processed data.
        """
        if self.keys is None:
            return {}
        for k in self.keys:
            try:
                input_data.pop(k)
            except:
                raise InputDataKeyError(k)
        return input_data


class Log(Action[Any, str]):
    """
    Logs message and current data
    """
    
    def __init__(
        self, 
        level: int=logging.NOTSET,
        logger: Optional[logging.Logger]=None, 
        message: str="",
        open: str="-"*40,
        close: str="-"*40,
        include_input_data: bool=True,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            level (int, optional): Logging level. Defaults to logging.NOTSET.

            logger (Optional[logging.Logger], optional): Logger object. 
                If value eqaules to None, evaluator logger will be used. Defaults to None

            message (str, optional): Message that will be logged. Defaults to "".
            
            open (str, optional): String that will be inserted before mesage(new line). 
                Defaults to "-"*40.
            
            close (str, optional): String that will be inserted after mesage(new line). 
                Defaults to "-"*40.
            
            include_input_data (bool, optional): Include data representation in log.
                Defaults to True.

            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.logger = logger
        self.level = level
        self.message = message
        self.open = open
        self.close = close
        self.include_input_data = include_input_data


    def execute(self, input_data: Any) -> str:
        """
        Create message string.

        Args:
            input_data (Any): Data for representation.

        Returns:
            str: Message for logging.
        """
        if self.include_input_data:
            return "\n".join((
                self.open, 
                self.message, 
                input_data.__repr__(), 
                self.close
            ))
        else:
            return "\n".join((
                self.open, 
                self.message, 
                self.close
            ))
    

    def __call__(
        self, 
        input_data: Transformable,
        evaluator: Optional[Evaluator]=None,
    ) -> Transformable:
        """
        Log call. Loggs data with provided logger or evaluator logger.

        Args:
            input_data (Transformable): Current data.

            evaluator (Optional[Evaluator], optional): Evaluator in context of wich action executed. 
                If equals to None, default evaluator will be created. Defaults to None.

        Returns:
            Transformable: Current data.
        """
        if not self.logger:
            if not evaluator:
                logger = self.set_up_default_evaluator()
            else:
                logger = evaluator
        else:
            logger = self.logger
        logger.log(self.level, self.execute(input_data))
        return input_data


class AddData(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Adds provided data to input data.
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
        Updates input data with provided data

        Args:
            input_data (Dict[str, Any]): Current data.

        Returns:
            Dict[str, Any]: Updated data.
        """
        input_data.update(self.data)
        return input_data


class RenameAttribute(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Renames specified key in input data.
    """
    def __init__(
        self, 
        old_name: str,
        new_name: str,
        name: Optional[str]=None
    ) -> None:
        """
        Args:
            old_name (str): Current name of the key.

            new_name (str): New name of the key.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.old_name = old_name
        self.new_name = new_name


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Renames key

        Args:
            input_data (Dict[str, Any]): Input data.

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
    Renames attributes keys using query string.
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
        super().__init__(name)
        self.query = query


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Renames keys using query.

        Args:
            input_data (Dict[str, Any]): Input data.

        Raises:
            InvalidQuery: Provided query is invalid.
            InputDataKeyError: Key for renaming doesn't exist.

        Returns:
            Dict[str, Any]: _description_
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
    Sets new value
    """
    def __init__(
        self, 
        key: str,
        value: Any,
        name: Optional[str]=None
    ) -> None:
        """
        Args:
            key (str): Key for wich new value will be seted.
            
            value (Any): New value.

            name (Optional[str], optional): name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.key = key
        self.value = value


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data[self.key] = self.value
        return input_data


class UnpackValue(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Unpacks value from nested level to current.
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
        super().__init__(name)
        self.key = key


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            data = input_data.pop(self.key)
        except:
            raise InputDataKeyError(self.key)
        if not isinstance(data, Dict):
            raise ValueError(f"Expected: Dict[str, Any]. Recieved value of type: {type(data)}")
        input_data.update(cast(Dict[str, Any], data))
        return input_data
    

class NestToKey(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Nests input data to specified key
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


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            self.key: input_data
        }


class ExecuteFunction(Action[ActionInput, ActionOutput]):
    """
    Executes provided function
    """
    def __init__(
        self, 
        f: Callable[[ActionInput], ActionOutput],
        name: Optional[str]=None,
        default_key: str="output",
    ) -> None:
        """
        Args:
            f (Callable[[ActionInput], ActionOutput]): Function for execution.

            name (Optional[str], optional): name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
            
            default_key (str, optional): Default key used for results that is not of type Dict.
                Defaults to "output".
        """
        super().__init__(
            name or f"{self.__class__.__name__}.{f.__name__}",
            default_key=default_key,
        )
        self.f = f


    def execute(self, input_data: ActionInput) -> ActionOutput:
        return self.f(input_data)