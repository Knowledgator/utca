from __future__ import annotations
from typing import (
    List, Callable, Optional, Tuple, Union
)
import copy
import logging

from core.executable_level_1.component import Component
from core.executable_level_1.schema import Transformable
from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.memory import GetMemory, MemoryGetInstruction
from core.exceptions import ExecutionSchemaFailed


class ExecutionSchema(Component):
    """
    Step by step execution of components
    """
    program: List[Component]

    def __init__(
        self, 
        comp: Optional[Component]=None, 
        name: Optional[str]=None
    ) -> None:
        """
        Args:
            comp (Optional[Component], optional): Initial Component. Defaults to None.

            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.program = []
        if comp:
            self.add(comp)
        

    def add(self, comp: Component) -> ExecutionSchema:
        """
        Add Component to the end

        Args:
            comp (Component): New component

        Returns:
            ExecutionSchema: self
        """
        self.program.append(comp)
        return self
    

    def __or__(self, component: Component) -> ExecutionSchema:
        """
        Adds component to ExecutionSchema

        Args:
            component (Component): New Component.

        Returns:
            ExecutionSchema: self
        """
        return self.add(component)
    

    def __call__(
        self, input_data: Transformable, evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        """
        Args:
            input_data (Transformable): Data that is used in action.
            
            evaluator (Optional[Evaluator], optional): Evaluator in context of wich ExecutionSchema
                executed. If equals to None, default evaluator will be created. Defaults to None.
        Raises:
            EvaluatorExecutionFailed: If any error occurs.

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

class Condition:
    """
    Condition class used to evaluation of intermediate data
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

            schema (Component): Intermidiate evaluation

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
            
            evaluator (Evaluator): Evaluator in context of wich Condition executed.

        Returns:
            bool: Result of evaluation. Define that condition is fulfilled or not.
        """
        if self.state != None:
            input_data = GetMemory(
                self.state, MemoryGetInstruction.GET
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
    Combines Condition and associated with it Component
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
            schema (Component): Associated Component

            condition (Optional[ConditionProtocol], optional): Associated Condition.
                If equals to None, always executed. Defaults to None.

            exit_branch (bool, optional): Specifies that this is last branch that 
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
        Evaluates Condition and if fulfilled executes Component

        Args:
            input_data (Transformable): Data for processing.

            evaluator (Evaluator): Evaluator in context of wich Branch executed.

        Returns:
            Optional[Transformable]: Result of executed Component.
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

            evaluator (Evaluator): Evaluator in context of wich Switch executed.

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
            
            set_key (Optional[str], optional): Data destnation. 
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

            evaluator (Evaluator): Evaluator in context of wich ForEach executed.

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
            
            set_key (Optional[str], optional): Data destnation. 
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

            evaluator (Evaluator): Evaluator in context of wich Filter executed.

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

            evaluator (Evaluator): Evaluator in context of wich While executed.

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
            input_data = self.schema(input_data, evaluator)
            i -= 1
        return input_data