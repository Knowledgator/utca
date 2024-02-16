from __future__ import annotations
import json
from typing import (
    List, Any, Dict, Type, Callable, TypeVar
)

from core.executable_level_1.component import Component
from core.executable_level_1.schema import Config 
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
    program: List[Dict[Statement, Any]]

    def __init__(self, comp: Component) -> None:
        self.program = []
        self.add(comp)
        

    def add(self, comp: Component) -> ExecutionSchema:
        statement = comp.generate_statement()
        self.program.append(statement)
        return self

    
    def retieve_program(self):
        return self.program
    

    def __or__(self, comp: Component) -> ExecutionSchema:
        return self.add(comp)


    def generate_statement(self) -> Dict[Statement, List[Dict[Statement, Any]]]:
        return {Statement.PIPELINE_STATEMENT: self.program}


class Loop(Component):
    loop: Component
    condition: Callable[[Dict[str, Any], int], bool]

    def __init__(
        self, 
        cfg: Config,
        loop: Component,
        condition: Callable[[Dict[str, Any], int], bool]
    ) -> None:
        self.loop = loop
        self.condition = condition
        super().__init__(cfg)


    def generate_statement(self) -> Dict[Statement, Any]:
        return {Statement.LOOP_STATEMENT: self.loop.generate_statement()}


class Path():
    condition: Callable[[Dict[str, Any]], bool] = lambda _: False
    executor: Component
    exit: bool = True


class Switch(Component):
    paths: List[Path]
    default: Path

    def __init__(self, cfg: Config, *path: Path, default: Path) -> None:
        self.paths = [*path]
        self.default = default
        super().__init__(cfg)

    
    def generate_statement(self) -> Dict[Statement, Dict[str, Any]]:
        return {
            Statement.SWITCH_STATEMENT: dict((
                *(
                    (path.condition.__name__, path.executor.generate_statement()) 
                    for path in self.paths
                ),
                ('default', self.default.executor.generate_statement())
            )),
        }


class Parallel(Component):
    paths: List[Component]

    def __init__(self, cfg: Config, *path: Component) -> None:
        self.paths = [*path]
        super().__init__(cfg)


    def generate_statement(self) -> Dict[Statement, List[Any]]:
        return {
            Statement.PARALLEL_STATEMENT: [
                path.generate_statement() for path in self.paths
            ]
        }


# program_structure = {
#     "start": [
#         {"statement": lambda ctx: print("Statement 1 execution", ctx)},
#         {"statement": lambda ctx: print("Statement 2 execution", ctx)},
#         {"if": {
#             "condition": lambda ctx: ctx["condition"],
#             "true_branch": [
#                 {"statement": lambda ctx: print("True branch statement", ctx)}
#             ],
#             "false_branch": [
#                 {"statement": lambda ctx: print("False branch statement", ctx)}
#             ]
#         }},
#         {"loop": {
#             "condition": lambda ctx: ctx["loop_condition"](),
#             "body": [
#                 {"statement": lambda ctx: print("Loop body statement", ctx) or ctx["loop_actions"]()}
#             ]
#         }}
#     ]
# }









