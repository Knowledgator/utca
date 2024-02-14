from __future__ import annotations
import json
from sys import executable
from typing import  Any, Dict, Optional, Type, TypeVar, Union, List, cast

from torch import StorageBase

from core.executable_level_1.component import Component
from core.executable_level_1.custom_exceptions import ExecutionSchemaInvalidFirstComponent, ExecutionSchemaInvalidFlow

from core.executable_level_1.executable import Executable
from core.executable_level_1.memory import GetMemory, SetMemory
from core.executable_level_1.schema import (
    Action, 
    Config, 
    Input,
    Output,
    Transformable,
)
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






# class IfStatement(Serializable): 
#     get_memory: GetMemory
#     bool_executable: Executable
#     right_branch: ExecuteStatement # how it can catch input
#     left_branch: ExecuteStatement


# class LoopStatement(Serializable):
#     condition: int 
#     child: ExecuteStatement


# class Function():
    # abstracts all this components - 4 primary
    pass
    # executable: Executable
    # set_memory: SetMemory
    # get_memory: GetMemory
    # transform: Transformable


# def generate_skelet() -> Dict[str, Any]:
#     return  {
#     "start": []
#     }





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









