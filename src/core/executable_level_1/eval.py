from typing import  Optional, Union, List, cast

from core.executable_level_1.component import Component
from core.executable_level_1.custom_exceptions import ExecutionSchemaInvalidFirstComponent, ExecutionSchemaInvalidFlow

from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import (
    Action, 
    Config, 
    Input,
    Output,
    Transformable,
)

TRANSFORM_STATEMENT = List[Union[Executable[Config, Input, Output], Action]]
INPUT_STATEMENT = List[Executable[Config, Input, Output]] # Executable Executable Executable
STATEMENT = Union[INPUT_STATEMENT, TRANSFORM_STATEMENT] # Action Action Action Action Executable
# STATEMENTs :  (write some notice)
# Input Statement : Input -> Executable->Transferable;
# Intermediate Statement : Transferable->Executable->Transferable;
# Output Statement :  Transferable->Executable->Output;

PROGRAM = List[STATEMENT]

# execute to execute protocol
# one to one
class Protocol():
    # mb start and end executable
    # ror scheck is it start or end + validation 
    ...


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



class EvaluatorConfigs():
    pass

# develop further as game engine ?
class Evaluator():
    program: PROGRAM
    transferable_checkpoint: Transformable
    
    def __init__(self, schema: ExecutionSchema, cfg: EvaluatorConfigs = EvaluatorConfigs()) -> None:
        self.program = schema.retieve_program()
    
    
    def run(self, program_input: Input):
        # execution loop
        for i, st in enumerate(self.program):
            if i == 0:
                self.execute_input_statement(st, program_input)
            else:
                self.execute_ordinary_statement(st)
            print("Executed step: ", i)
        return self.transferable_checkpoint.extract()
    

    def execute_ordinary_statement(self, statement: TRANSFORM_STATEMENT):
        for el in statement:
            if  isinstance(el, Executable):
                self.transferable_checkpoint = el.execute(self.transferable_checkpoint, Transformable)
            else:
                self.transferable_checkpoint.update_state(el)


    def execute_input_statement(self, statement: INPUT_STATEMENT, input: Input):
        executable = statement[0]
        self.transferable_checkpoint = executable.execute(input, Transformable)





# transformable can NOT be done on static fold
# how it can dynamic change ?


# class Pipeline():
#     last_exec: Executable[Config, Input, Output]
#     def __ror__(self, __value: Union[Executable[ConfigType, InputType, OutputType], Transformable])-> int:
#         # add 2 pipelines
#         return 3
#     def __call__(self, *args: Any, **kwds: Any) -> Any:
#         pass
#     def run(self) -> None:
#         pass
    
#     def run_protocol(self):

#         pass




