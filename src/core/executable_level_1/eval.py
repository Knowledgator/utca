from __future__ import annotations
import json
from typing import (
    List, Callable, Optional, Tuple, Type,  TypeVar, Union
)

from core.executable_level_1.component import Component
from core.executable_level_1.schema import Transformable
from core.executable_level_1.statements_types import Statement

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

    
    def retrieve_program(self) -> List[Component]:
        return self.program
    

    def __or__(self, comp: Component) -> ExecutionSchema:
        return self.add(comp)


    @property
    def statement(self) -> Statement:
        return Statement.PIPELINE_STATEMENT


class Condition():
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

    
    def get_state(self):
        return self.state
    

    def get_validator(self):
        return self.validator
    

    def get_statement(self):
        return self.schema
    

    @property
    def statement(self) ->  Statement:
        return Statement.CONDITION


class IfStatement(Component):
    condition: Union[Callable[[Transformable], bool], Condition]
    # executed if true 
    right_statement: ExecutionSchema
    # executed if false 
    left_statement: Optional[ExecutionSchema]

    def __init__(
        self, 
        condition: Union[Callable[[Transformable], bool], Condition],
        right_statement: ExecutionSchema,
        left_statement: Optional[ExecutionSchema]=None
        ) -> None:
        # add conditional
        if isinstance(condition, Condition):
            self.condition = condition
        else:
            condition = condition
        # add statements
        self.right_statement = right_statement
        if left_statement == None:
            self.left_statement = None
        else:
            self.left_statement = left_statement


    def get_condition(self):
        return self.condition


    def get_right_statement(self):
        return self.right_statement 


    def get_left_statement(self):
        return self.left_statement 


    @property
    def statement(self) ->  Statement:
        return Statement.IF_STATEMENT


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


    def get_statement(self) -> ExecutionSchema:
        return self.schema
    
    
    @property
    def statement(self) ->  Statement:
        return Statement.FOR_EACH_STATEMENT


class Filter(Component):
    get_key: str
    set_key: str
    condition: Union[Callable[[Transformable], bool], Condition]

    def __init__(
        self,
        condition: Union[Callable[[Transformable], bool], Condition],
        get_key: str,
        set_key: Optional[str]=None,
    ) -> None:
        self.get_key = get_key
        self.set_key = set_key or get_key
        self.condition = condition


    def get_condition(self) -> Union[Callable[[Transformable], bool], Condition]:
        return self.condition
    
    
    @property
    def statement(self) ->  Statement:
        return Statement.FILTER_STATEMENT



class While(Component):
    schema: ExecutionSchema
    condition:  Condition
    max_retries: Optional[int]

    def __init__(
        self, 
        condition: Condition,
        statement: ExecutionSchema,
        max_retries: Optional[int]
        ) -> None:
        # add conditional
        self.condition = condition

        # add statements
        self.schema = statement
        self.max_retries = max_retries


    def get_retries(self):
        return self.max_retries


    def get_condition(self):
        return self.condition


    def get_statement(self):
        return self.schema


    @property
    def statement(self) ->  Statement:
        return Statement.WHILE_STATEMEMT