from __future__ import annotations
import json
from typing import (
    List, Callable, Optional, Tuple, Type,  TypeVar, Union, Protocol
)
import copy

from core.executable_level_1.component import Component
from core.executable_level_1.schema import Transformable
from core.executable_level_1.interpreter import Evaluator, EvaluatorConfigs
from core.executable_level_1.memory import GetMemory, MemoryGetInstruction
from exceptions import EvaluatorExecutionFailed

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

    def __init__(self, comp: Component) -> None:
        self.program = []
        self.add(comp)
        

    def add(self, comp: Component) -> ExecutionSchema:
        self.program.append(comp)
        return self
    

    def __or__(self, comp: Component) -> ExecutionSchema:
        return self.add(comp)
    

    def __call__(
        self, input_data: Transformable, evaluator: Evaluator
    ) -> Transformable:
        for i, component in enumerate(self.program):
            try:
                input_data = component(input_data, evaluator)
                evaluator.cfg.logger.info(
                    f"{self.__class__.__name__}: Step {i} executed successfully."
                )
            except Exception as e:
                evaluator.cfg.logger.error(f"{self.__class__.__name__}: Error at step {i}")
                evaluator.cfg.logger.exception(e)
                if evaluator.cfg.fast_exit:
                    raise EvaluatorExecutionFailed(e)
        return input_data


class ConditionType(Protocol):
    def __call__(
        self, input_data: Transformable, evaluator: Evaluator
    ) -> bool:
        ...


class Condition:
    validator: Callable[[Transformable], bool]
    schema: ExecutionSchema
    state: Optional[List[Union[str, Tuple[str, str]]]]

    def __init__(
        self, 
        validator: Callable[[Transformable], bool],
        statement: ExecutionSchema,
        state: Optional[List[Union[str, Tuple[str, str]]]]=None
    ) -> None:
        self.validator = validator
        self.schema = statement
        self.state = state
    

    def __call__(
        self, input_data: Transformable, evaluator: Evaluator
    ) -> bool:
        if self.state != None:
            input_data = GetMemory(
                self.state, MemoryGetInstruction.GET
            )(
                input_data, evaluator
            )
            
        tmp = (
            evaluator
            .create_child(self.schema, self.__class__.__name__)
            .eval(copy.deepcopy(input_data))
        )
        return self.validator(tmp)


class BranchStatement:
    condition: Optional[ConditionType]
    schema: Component
    exit_branch: bool

    def __init__(
        self, 
        schema: Component,
        condition: Optional[ConditionType]=None, 
        exit_branch: bool=True
    ):
        self.condition = condition
        self.schema = schema
        self.exit_branch = exit_branch


    def __call__(
        self, input_data: Transformable, evaluator: Evaluator
    ) -> Optional[Transformable]:
        if self.condition is None or self.condition(
            input_data, evaluator
        ):
            return self.schema(input_data, evaluator)


class SwitchStatement(Component):
    branches: Tuple[BranchStatement, ...]

    def __init__(
        self, 
        *branches: BranchStatement,
    ) -> None:
        self.branches = branches


    def __call__(self, input_data: Transformable, evaluator: Evaluator) -> Transformable:
        for branch in self.branches:
            if res := branch(input_data, evaluator):
                input_data = res
                if branch.exit_branch:
                    break
        return input_data


class ForEach(Component):
    schema: ExecutionSchema

    def __init__(
        self, 
        statement: ExecutionSchema,
        get_key: str,
        set_key: Optional[str]=None,
    ) -> None:
        self.get_key = get_key
        self.set_key = set_key or get_key
        self.schema = statement


    def __call__(self, input_data: Transformable, evaluator: Evaluator) -> Transformable:
        data = getattr(input_data, self.get_key)
        # need check that this is a sequence of dict

        setattr(
            input_data,
            self.set_key,
            [
                Evaluator(
                    self.schema,
                    cfg=EvaluatorConfigs(
                        name=f"{evaluator.cfg.name}.{self.__class__.__name__}",
                        logging_level=evaluator.cfg.logging_level,
                        logging_handler=evaluator.cfg.logging_handler,
                        fast_exit=evaluator.cfg.fast_exit
                    )
                ).run_program(t)
                for t in data
            ]
        )
        return input_data
    

class Filter(Component):
    get_key: str
    set_key: str
    condition: ConditionType

    def __init__(
        self,
        condition: ConditionType,
        get_key: str,
        set_key: Optional[str]=None,
    ) -> None:
        self.get_key = get_key
        self.set_key = set_key or get_key
        self.condition = condition


    def __call__(
        self, input_data: Transformable, evaluator: Evaluator
    ) -> Transformable:
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
    schema: ExecutionSchema
    condition:  Condition
    max_iterations: int

    def __init__(
        self, 
        condition: Condition,
        schema: ExecutionSchema,
        max_iterations: int=-1
    ) -> None:
        self.condition = condition
        self.schema = schema
        self.max_iterations = max_iterations


    def __call__(
        self, input_data: Transformable, evaluator: Evaluator
    ) -> Transformable:
        i = self.max_iterations
        while i != 0 and self.condition(
            input_data,
            evaluator
        ):
            input_data = self.schema(input_data, evaluator)
            i -= 1
        return input_data