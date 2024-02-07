from typing import  Optional, Union, List

from core.executable_level_1.component import Component
from core.executable_level_1.custom_exceptions import ExecutionSchemaInvalidFirstComponent, ExecutionSchemaInvalidFlow

from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import  Action, AddData, ChangeValue, Config, Input,  MergeData, Output,RenameAttribute, RenameAttributeQuery, Transformable


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
    @classmethod
    def handle_transform(cls, transform: Transformable, action: Action):
        if isinstance(action, AddData):
            transform.add_data(action.get_data())
        elif isinstance(action, RenameAttribute):
            transform.rename_state_attr(action.old_name, action.old_name)
        elif isinstance(action, RenameAttributeQuery):
            transform.rename_state_attr_q(action.query)
        elif isinstance(action, MergeData):
            transform.merge_state(action.get_data(), action.is_new_priority())
        elif isinstance(action, ChangeValue):
            transform.change_value(action.get_key(), action.get_value())
        return transform

class ExecutionSchema():
    last_executable: Optional[Executable[Config, Input, Output]] = None
    actions: List[Action]
    statements: PROGRAM
    def __init__(self, comp: Component) -> None:
        if comp is Executable[Config, Input, Output]:
            self.last_executable = comp
            self.create_input_statement(comp)
        else:
            raise ExecutionSchemaInvalidFirstComponent
    def add(self, comp: Component):
        if comp is Action:
            self.actions.append(comp)
        if comp is Executable:
            if self.last_executable != None:
                self.create_statement(comp)
                self.last_executable = comp
            else:
                raise ExecutionSchemaInvalidFlow
    def create_input_statement(self, comp: Executable[Config, Input, Output]):
         new_statement: STATEMENT  = []
         new_statement.append(comp)
         self.statements.append(new_statement)
    def create_statement(self, executable: Executable[Config, Input, Output]):
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
        self.schema: PROGRAM = schema.retieve_program()
    def run(self, program_input: Input):
        # execution loop

        for i, st in enumerate(self.program):
            if st is INPUT_STATEMENT:
                self.execute_input_statement(st, program_input)
            if st is TRANSFORM_STATEMENT:
                self.execute_ordinary_statement(st)
            print("Executed step: ", i)

    def execute_ordinary_statement(self, statement: TRANSFORM_STATEMENT):
        for el in statement:
            if  isinstance(el, Executable):
                self.transferable_checkpoint = el.execute(self.transferable_checkpoint, Transformable)
            else:
                Protocol.handle_transform(self.transferable_checkpoint, el)

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




