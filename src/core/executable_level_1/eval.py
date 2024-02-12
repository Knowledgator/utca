from typing import  Optional, Union, List, cast

from core.executable_level_1.component import Component
from core.executable_level_1.custom_exceptions import ExecutionSchemaInvalidFirstComponent, ExecutionSchemaInvalidFlow

from core.executable_level_1.executable import Executable
from core.executable_level_1.memory import Memory
from core.executable_level_1.schema import (
    Action, 
    Config, 
    Input,
    Output,
    Transformable,
)

# Program tree, where statements are actions
# {
#     [Statement]
# }
# There should be restart sign  + offset

# rework this classes

TRANSFORM_STATEMENT = List[Union[Executable[Config, Input, Output], Action]]
INPUT_STATEMENT = List[Executable[Config, Input, Output]] # Executable Executable Executable
STATEMENT = Union[INPUT_STATEMENT, TRANSFORM_STATEMENT] # Action Action Action Action Executable
# STATEMENTs :  (write some notice)
# Input Statement : Input -> Executable->Transferable;
# Intermediate Statement : Transferable->Executable->Transferable;
# Output Statement :  Transferable->Executable->Output;

PROGRAM = List[STATEMENT]




class ExecutionSchema():
    last_executable: Optional[Executable[Config, Input, Output]] = None
    actions: List[Action]
    statements: PROGRAM

    def __init__(self, comp: Component) -> None:
        self.statements = []
        self.actions = []
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















