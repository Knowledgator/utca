from __future__ import annotations
from typing import (
    Any, List, Callable, Optional, Tuple, Union
)
import copy
import logging

from utca.core.executable_level_1.component import Component
from utca.core.executable_level_1.schema import Transformable
from utca.core.executable_level_1.interpreter import Evaluator
from utca.core.executable_level_1.memory import GetMemory, MemoryGetInstruction
from utca.core.exceptions import ExecutionSchemaFailed, ExitLoop


class ExecutionSchema(Component):
    """
    Step by step execution of components
    """
    program: List[Component]

    def __init__(
        self, 
        component: Optional[Component]=None, 
        name: Optional[str]=None
    ) -> None:
        """
        Args:
            component (Optional[Component], optional): Initial Component. Defaults to None.

            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.program = []
        if component:
            self.add(component)
        

    def add(self, component: Component) -> ExecutionSchema:
        """
        Add Component to the end

        Args:
            component (Component): New component.

        Returns:
            ExecutionSchema: self.
        """
        self.program.append(component)
        return self
    

    def __or__(self, component: Component) -> ExecutionSchema:
        """
        Add Component to ExecutionSchema

        Args:
            component (Component): New Component.

        Returns:
            ExecutionSchema: self.
        """
        return self.add(component)
    

    def __call__(
        self, input_data: Transformable, evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        """
        Args:
            input_data (Transformable): Data that is used in action.
            
            evaluator (Optional[Evaluator], optional): Evaluator in context of which ExecutionSchema
                executed. If equals to None, default evaluator will be created. Defaults to None.
        Raises:
            ExecutionSchemaFailed: If any error occurs.

        Returns:
            Transformable: Result of execution.
        """
        if not evaluator:
            evaluator = self.set_up_default_evaluator()

        for i, component in enumerate(self.program):
            try:
                input_data = component(input_data, evaluator)
                evaluator.log(
                    logging.INFO,
                    f"{self.name}: Step {i}({component.name}) executed successfully."
                )
            except ExitLoop as e:
                raise e
            except Exception as e:
                evaluator.log(
                    logging.ERROR,
                    f"{self.name}: Error at step {i}"
                )
                evaluator.log(logging.ERROR, e, exc_info=True)
                if evaluator.fast_exit:
                    raise ExecutionSchemaFailed(self.name, e)
        return input_data


ConditionProtocol = Callable[[Transformable, Evaluator], bool]
"""
Type that describes objects that can be used as conditions and validators in Condition
"""

class Condition:
    """
    Condition class used for evaluation of intermediate data
    """
    validator: ConditionProtocol
    schema: Component
    state: Optional[List[Union[str, Tuple[str, str]]]]

    def __init__(
        self, 
        validator: ConditionProtocol,
        schema: Component,
        state: Optional[List[Union[str, Tuple[str, str]]]]=None,
        name: Optional[str]=None
    ) -> None:
        """
        Args:
            validator (ConditionProtocol): Callable that returns bool value that define
                that condition is fulfilled or not.

            schema (Component): Intermidiate evaluation.

            state (Optional[List[Union[str, Tuple[str, str]]]], optional): Memory keys that will be used. 
                If equals to None, memory will not be used. Defaults to None.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        self.validator = validator
        self.schema = schema
        self.state = state
        self.name = name or self.__class__.__name__
    

    def __call__(
        self, input_data: Transformable, evaluator: Evaluator
    ) -> bool:
        """
        Args:
            input_data (Transformable): Data for processing
            
            evaluator (Evaluator): Evaluator in context of which Condition executed.

        Returns:
            bool: Result of evaluation. Define that condition is fulfilled or not.
        """
        if self.state != None:
            input_data = GetMemory(
                self.state, memory_instruction=MemoryGetInstruction.GET
            )(
                input_data, evaluator
            )
        return self.validator(
            evaluator
            .create_child(self.schema, self.name)(copy.copy(input_data), evaluator),
            evaluator
        )
    

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.name} ({self.__dict__})"


class Branch:
    """
    Combination of condition and associated with it Component
    """
    condition: Optional[ConditionProtocol]
    schema: Component
    exit_branch: bool

    def __init__(
        self, 
        schema: Component,
        condition: Optional[ConditionProtocol]=None, 
        exit_branch: bool=True,
        name: Optional[str]=None
    ) -> None:
        """
        Args:
            schema (Component): Associated Component.

            condition (Optional[ConditionProtocol], optional): Associated condition.
                If equals to None, schema always executed. Defaults to None.

            exit_branch (bool, optional): Specifies that this is the last branch that 
                should be executed. Defaults to True.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        self.condition = condition
        self.schema = schema
        self.exit_branch = exit_branch
        self.name = name


    def __call__(
        self, input_data: Transformable, evaluator: Evaluator
    ) -> Optional[Transformable]:
        """
        Evaluates condition and, if fulfilled, executes schema

        Args:
            input_data (Transformable): Data for processing.

            evaluator (Evaluator): Evaluator in context of which Branch executed.

        Returns:
            Optional[Transformable]: Result of executed schema, if executed; otherwise, None.
        """
        if self.condition is None or self.condition(
            input_data, evaluator
        ):
            return self.schema(input_data, evaluator)
        

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.name} ({self.__dict__})"


class Switch(Component):
    """
    Variable execution defined by input data
    """
    branches: Tuple[Branch, ...]

    def __init__(
        self, 
        *branches: Branch,
        name: Optional[str]=None
    ) -> None:
        """
        Args:
            *branches (Branch): Branches that will be used.

            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.branches = branches


    def __call__(
        self, input_data: Transformable, evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        """
        Args:
            input_data (Transformable): Data for processing.

            evaluator (Optional[Evaluator], optional): Evaluator in context of which Switch
                executed. If equals to None, default evaluator will be created. Defaults to None.

        Returns:
            Transformable: Result of execution.
        """
        if not evaluator:
            evaluator = self.set_up_default_evaluator()
        
        for branch in self.branches:
            if res := branch(input_data, evaluator):
                input_data = res
                if branch.exit_branch:
                    break
        return input_data


class ForEach(Component):
    """
    Execution for each item in data series
    """
    schema: Component

    def __init__(
        self, 
        schema: Component,
        get_key: str,
        set_key: Optional[str]=None,
        name: Optional[str]=None
    ) -> None:
        """
        Args:
            schema (Component): Component that will be executed.
            
            get_key (str): Key associated with series of data items.
            
            set_key (Optional[str], optional): Data destination. 
                If equals to None, get_key will be used. Defaults to None.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.get_key = get_key
        self.set_key = set_key or get_key
        self.schema = schema


    def __call__(
        self, input_data: Transformable, evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        """
        Args:
            input_data (Transformable): Data for processing.

            evaluator (Optional[Evaluator], optional): Evaluator in context of which ForEach
                executed. If equals to None, default evaluator will be created. Defaults to None.

        Returns:
            Transformable: Result of execution.
        """
        if not evaluator:
            evaluator = self.set_up_default_evaluator()
        
        data = getattr(input_data, self.get_key)

        setattr(
            input_data,
            self.set_key,
            [
                evaluator.create_child(self.schema, self.name).run(copy.copy(t), evaluator)
                for t in data
            ]
        )
        return input_data
    

class Filter(Component):
    """
    Filters data series by fulfilling of condition
    """
    get_key: str
    set_key: str
    condition: ConditionProtocol

    def __init__(
        self,
        condition: ConditionProtocol,
        get_key: str,
        set_key: Optional[str]=None,
        name: Optional[str]=None
    ) -> None:
        """
        Args:
            condition (ConditionProtocol): Filter condition.

            get_key (str): Key associated with series of data items.
            
            set_key (Optional[str], optional): Data destination. 
                If equals to None, get_key will be used. Defaults to None.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.get_key = get_key
        self.set_key = set_key or get_key
        self.condition = condition


    def __call__(
        self, input_data: Transformable, evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        """
        Args:
            input_data (Transformable): Data for processing.

            evaluator (Optional[Evaluator], optional): Evaluator in context of which Filter
                executed. If equals to None, default evaluator will be created. Defaults to None.

        Returns:
            Transformable: Result of execution.
        """
        if not evaluator:
            evaluator = self.set_up_default_evaluator()

        data = getattr(input_data, self.get_key)
        setattr(
            input_data,
            self.set_key,
            [
                s for s in data
                if self.condition(Transformable(s), evaluator)
            ]
        )
        return input_data


class While(Component):
    """
    Loop execution based on condition and/or iterations
    """
    schema: Component
    condition:  Optional[ConditionProtocol]=None
    max_iterations: int

    def __init__(
        self, 
        schema: Component,
        condition: Optional[ConditionProtocol]=None,
        max_iterations: int=-1,
        name: Optional[str]=None
    ) -> None:
        """
        Args:
            schema (Component): Component that will be executed.

            condition (Optional[ConditionProtocol], optional): Condition for loop execution. 
                If equals to None, loop will not be bounded by condition. Defaults to None.
            
            max_iterations (int, optional): Maximum iterations before exit.
                If equals to -1, will not be bounded by number of iterations. Defaults to -1.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.condition = condition
        self.schema = schema
        self.max_iterations = max_iterations
        if not condition and max_iterations < 0:
            logging.warning(f"While: {self.name}: Loop is not bounded!")


    def __call__(
        self, input_data: Transformable, evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        """
        Args:
            input_data (Transformable): Data for processing.

            evaluator (Optional[Evaluator], optional): Evaluator in context of which While
                executed. If equals to None, default evaluator will be created. Defaults to None.

        Returns:
            Transformable: Result of execution.
        """
        if not evaluator:
            evaluator = self.set_up_default_evaluator()
            
        i = self.max_iterations
        while i != 0 and (not self.condition or self.condition(
            input_data,
            evaluator
        )):
            try:
                input_data = self.schema(input_data, evaluator)
            except ExitLoop:
                break
            i -= 1
        return input_data
    

class Break(Component):
    """
    Exit loop
    """
    def __call__(
        self, _: Transformable, __: Optional[Evaluator]=None
    ) -> Transformable:
        raise ExitLoop
    
BREAK = Break()
"""Exit loop singleton"""

class Log(Component):
    """
    Log message and current data
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


    def create_message(self, input_data: Any) -> str:
        """
        Create message string

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

            evaluator (Optional[Evaluator], optional): Evaluator in context of which action executed. 
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
        logger.log(self.level, self.create_message(input_data))
        return input_data