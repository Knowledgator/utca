from __future__ import annotations
import json
from typing import (
    Callable, List, Any, Dict, Optional, Type,  TypeVar, Union
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
    program: List[Dict[str, Any]]

    def __init__(self, comp: Component) -> None:
        self.program = []
        self.add(comp)
        

    def add(self, comp: Component) -> ExecutionSchema:
        statement: Dict[str, Any] = comp.generate_statement()
        self.program.append(statement)
        return self

    
    def retrieve_program(self) -> List[Dict[str, Any]]:
        return self.program
    

    def __or__(self, comp: Component) -> ExecutionSchema:
        return self.add(comp)


    def generate_statement(self) -> Dict[str, Any]:
        return {"type": Statement.PIPELINE_STATEMENT, Statement.PIPELINE_STATEMENT.value: self.program}

# indicator (condition) ? function
class Condition():
    validator: Callable[[Transformable], bool]
    statement: ExecutionSchema
    state: List[str] | None
    def __init__(
        self, 
        validator: Callable[[Transformable], bool],
        statement: ExecutionSchema,
        state: Optional[List[str]]
    ) -> None:
        self.validator = validator
        self.statement = statement
        self.constatementition: Dict[str, Any] = statement.generate_statement()
        self.state = state

    
    def get_state(self):
        return self.state
    def get_validator(self):
        return self.validator
    def get_statement(self):
        return self.statement
    def generate_statement(self) ->  Dict[str, Any]:
        return {"type": Statement.CONDITION, Statement.CONDITION.value: self}


class IfStatement(Component):
    condition: Union[Callable[[Transformable], bool], Condition]
    # executed if true 
    right_statement: Dict[str, Any]
    # executed if false 
    left_statement: Dict[str, Any] | None
    def __init__(
        self, 
        condition: Union[Callable[..., bool], Condition],
        right_statement: ExecutionSchema,
        left_statement: ExecutionSchema | None
        ) -> None:
        # add conditional
        if isinstance(condition, Condition):
            self.condition = condition
        else:
            condition = condition
        # add statements
        self.right_statement = right_statement.generate_statement()
        if left_statement == None:
            self.left_statement = None
        else:
            self.left_statement = left_statement.generate_statement()

    def get_condition(self):
        return self.condition

    def get_right_statement(self):
        return self.right_statement 
    
    def get_left_statement(self):
        return self.left_statement 

    def generate_statement(self) ->  Dict[str, Any]:
        return {"type": Statement.IF_STATEMENT, Statement.IF_STATEMENT.value: self}


class ForEach(Component):
    statement: ExecutionSchema

    def __init__(self, statement: ExecutionSchema) -> None:
        self.statement = statement


    def get_statement(self) -> ExecutionSchema:
        return self.statement
    
    
    def generate_statement(self) ->  Dict[str, Any]:
        return {
            "type": Statement.FOR_EACH_STATEMENT, 
            Statement.FOR_EACH_STATEMENT.value: self
        }
    

class Filter(Component):
    condition: Union[Callable[..., bool], Condition]

    def __init__(self, condition: Union[Callable[..., bool], Condition]) -> None:
        self.condition = condition


    def get_condition(self) -> Union[Callable[..., bool], Condition]:
        return self.condition
    
    
    def generate_statement(self) ->  Dict[str, Any]:
        return {
            "type": Statement.FILTER_STATEMENT, 
            Statement.FILTER_STATEMENT.value: self
        }



class While(Component):
    statement: Dict[str, Any]
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
        self.statement = statement.generate_statement()
        self.max_retries = max_retries
    def get_retries(self):
        return self.max_retries
    def get_condition(self):
        return self.condition
    def get_statement(self):
        return self.statement 
    def generate_statement(self) ->  Dict[str, Any]:
        return {"type": Statement.WHILE_STATEMEMT, Statement.WHILE_STATEMEMT.value: self}

# class Path():
#     condition: Callable[[Dict[str, Any]], bool] = lambda _: False
#     executor: Component
#     exit: bool = True


# class Switch(Component):
#     paths: List[Path]
#     default: Path

#     def __init__(self, cfg: Config, *path: Path, default: Path) -> None:
#         self.paths = [*path]
#         self.default = default
#         super().__init__(cfg)

    
#     def generate_statement(self) -> Dict[Statement, Dict[str, Any]]:
#         return {
#             Statement.SWITCH_STATEMENT: dict((
#                 *(
#                     (path.condition.__name__, path.executor.generate_statement()) 
#                     for path in self.paths
#                 ),
#                 ('default', self.default.executor.generate_statement())
#             )),
#         }


# class Parallel(Component):
#     paths: List[Component]

#     def __init__(self, cfg: Config, *path: Component) -> None:
#         self.paths = [*path]
#         super().__init__(cfg)


#     def generate_statement(self) -> Dict[Statement, List[Any]]:
#         return {
#             Statement.PARALLEL_STATEMENT: [
#                 path.generate_statement() for path in self.paths
#             ]
#         }












