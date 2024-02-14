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


class Statement():
    @staticmethod
    def create_execute_statement():
        pass


class ExecuteStatement():
    @staticmethod
    def create_execute_statement():
        return {"type": "execute_statement", }


class TransformStatement():




class InputStatement(Serializable):

    executable: Executable
    input: Input
    def __init__(self) -> None:
        pass




class IfStatement(Serializable): 
    get_memory: GetMemory
    bool_executable: Executable
    right_branch: ExecuteStatement # how it can catch input
    left_branch: ExecuteStatement


class LoopStatement(Serializable):
    condition: int 
    child: ExecuteStatement


class Function():
    # abstracts all this components - 4 primary
    pass
    # executable: Executable
    # set_memory: SetMemory
    # get_memory: GetMemory
    # transform: Transformable

TRANSFORM_STATEMENT = List[Union[Executable[Config, Input, Output], Action]]
INPUT_STATEMENT = List[Executable[Config, Input, Output]] # Executable Executable Executable
STATEMENT = Union[INPUT_STATEMENT, TRANSFORM_STATEMENT] # Action Action Action Action Executable
# STATEMENTs :  (write some notice)
# Input Statement : Input -> Executable->Transferable;
# Intermediate Statement : Transferable->Executable->Transferable;
# Output Statement :  Transferable->Executable->Output;

PROGRAM: Dict[str, Any]= {
    "start": []
}



class ExecutionSchema():
    program: Dict[str, Any]

    def __init__(self, comp: Component) -> None:
        self.program = PROGRAM
        
        if isinstance(comp, Executable):
            self.last_executable = comp
            comp = cast(Executable[Config, Input, Output], comp)
            self.create_input_statement(comp)
        else:
            raise ExecutionSchemaInvalidFirstComponent
        

    def add(self, comp: Component):
        if isinstance(comp, Action):
            self.actions.append(comp)
        elif isinstance(comp, Executable):
            if self.last_executable != None:
                comp = cast(Executable[Config, Input, Output], comp)
                self.create_statement(comp)
                self.last_executable = comp
                self.actions = []
            else:
                raise ExecutionSchemaInvalidFlow()
        else:
            raise ValueError(comp)
    
    
    def create_input_statement(
        self, comp: Executable[Config, Input, Output]
    ):
        new_statement: STATEMENT  = []
        new_statement.append(comp)
        self.statements.append(new_statement)


    def create_statement(
        self, executable: Executable[Config, Input, Output]
    ):
        # EXECUTABLE + ACTION
        new_statement: STATEMENT  = []
        new_statement = new_statement + self.actions
        new_statement.append(executable)
        self.statements.append(new_statement)
    
    
    def retieve_program(self):
        return self.statements















