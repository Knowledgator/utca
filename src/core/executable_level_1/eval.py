from __future__ import annotations
import json
from typing import (
    List, Callable, Optional, Tuple, Type,  TypeVar, Union
)
import copy
import logging

from core.executable_level_1.component import Component
from core.executable_level_1.schema import Transformable
from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.memory import GetMemory, MemoryGetInstruction
from core.exceptions import EvaluatorExecutionFailed

T = TypeVar('T', bound='Serializable')

class Serializable:
    def to_json(self) -> str:
        """
        Serialize the object to a JSON string.
        """
        return json.dumps(self.__dict__, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @classmethod
    def from_json(cls: Type[T], json_str: str) -> T:
        """
        Deserialize a JSON string to an object of the class.

        :param json_str: A JSON string representing the object.
        :return: An instance of the class with attributes set according to the JSON string.
        """
        attributes = json.loads(json_str)
        obj = cls()  
        obj.__dict__.update(attributes)
        return obj


class ExecutionSchema(Component):
    program: List[Component]

    def __init__(
        self, 
        comp: Optional[Component]=None, 
        name: Optional[str]=None
    ) -> None:
        super().__init__(name)
        self.program = []
        if comp:
            self.add(comp)
        

    def add(self, comp: Component) -> ExecutionSchema:
        self.program.append(comp)
        return self
    

    def __or__(self, comp: Component) -> ExecutionSchema:
        return self.add(comp)
    

    def __call__(
        self, input_data: Transformable, evaluator: Optional[Evaluator]=None
    ) -> Transformable:
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
                if evaluator.cfg.fast_exit:
                    raise EvaluatorExecutionFailed(e)
        return input_data


ConditionProtocol = Callable[[Transformable, Evaluator], bool]

class Condition:
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
        self.validator = validator
        self.schema = schema
        self.state = state
        self.name = name or self.__class__.__name__
    

    def __call__(
        self, input_data: Transformable, evaluator: Evaluator
    ) -> bool:
        if self.state != None:
            input_data = GetMemory(
                self.state, MemoryGetInstruction.GET
            )(
                input_data, evaluator
            )
        return self.validator(
            evaluator
            .create_child(self.schema, self.name)
            .eval(copy.deepcopy(input_data)),
            evaluator
        )
    

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.name} ({self.__dict__})"


class Branch:
    condition: Optional[ConditionProtocol]
    schema: Component
    exit_branch: bool

    def __init__(
        self, 
        schema: Component,
        condition: Optional[ConditionProtocol]=None, 
        exit_branch: bool=True,
        name: Optional[str]=None
    ):
        self.condition = condition
        self.schema = schema
        self.exit_branch = exit_branch
        self.name = name


    def __call__(
        self, input_data: Transformable, evaluator: Evaluator
    ) -> Optional[Transformable]:
        if self.condition is None or self.condition(
            input_data, evaluator
        ):
            return self.schema(input_data, evaluator)
        

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.name} ({self.__dict__})"


class Switch(Component):
    branches: Tuple[Branch, ...]

    def __init__(
        self, 
        *branches: Branch,
        name: Optional[str]=None
    ) -> None:
        super().__init__(name)
        self.branches = branches


    def __call__(
        self, input_data: Transformable, evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        if not evaluator:
            evaluator = self.set_up_default_evaluator()
        
        for branch in self.branches:
            if res := branch(input_data, evaluator):
                input_data = res
                if branch.exit_branch:
                    break
        return input_data


class ForEach(Component):
    schema: Component

    def __init__(
        self, 
        schema: Component,
        get_key: str,
        set_key: Optional[str]=None,
        name: Optional[str]=None
    ) -> None:
        super().__init__(name)
        self.get_key = get_key
        self.set_key = set_key or get_key
        self.schema = schema


    def __call__(
        self, input_data: Transformable, evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        if not evaluator:
            evaluator = self.set_up_default_evaluator()
        
        data = getattr(input_data, self.get_key)
        # need check that this is a sequence of dict

        setattr(
            input_data,
            self.set_key,
            [
                evaluator.create_child(self.schema, self.name).run(copy.deepcopy(t))
                for t in data
            ]
        )
        return input_data
    

class Filter(Component):
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
        super().__init__(name)
        self.get_key = get_key
        self.set_key = set_key or get_key
        self.condition = condition


    def __call__(
        self, input_data: Transformable, evaluator: Optional[Evaluator]=None
    ) -> Transformable:
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
    schema: Component
    condition:  ConditionProtocol
    max_iterations: int

    def __init__(
        self, 
        condition: ConditionProtocol,
        schema: Component,
        max_iterations: int=-1,
        name: Optional[str]=None
    ) -> None:
        super().__init__(name)
        self.condition = condition
        self.schema = schema
        self.max_iterations = max_iterations


    def __call__(
        self, input_data: Transformable, evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        if not evaluator:
            evaluator = self.set_up_default_evaluator()
            
        i = self.max_iterations
        while i != 0 and self.condition(
            input_data,
            evaluator
        ):
            input_data = self.schema(input_data, evaluator)
            i -= 1
        return input_data