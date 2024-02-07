from typing import  Optional, Union, List

from core.executable_level_1.component import Component
from core.executable_level_1.custom_exceptions import ExecutionSchemaInvalidFirstComponent

from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import  Action, AddData, ChangeValue, Config, Input,  MergeData, Output,RenameAttribute, RenameAttributeQuery, Transformable


STATEMENT = List[Union[Executable[Config, Input, Output], Action]]

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
    
    def __init__(self, component: Component) -> None:
        if component is Executable[Config, Input, Output]:
            self.last_executable = component
        else:
            raise ExecutionSchemaInvalidFirstComponent
    def add(self, comp: Component):
        if comp is Action:
            self.actions.append(comp)
        if comp is Executable:
            if self.last_executable != None:
                self.create_statement(comp)
                self.last_executable = None
            else:
                self.last_executable = comp

    def create_statement(self, executable: Executable[Config, Input, Output]):
        new_statement: STATEMENT  = []
        new_statement.append(self.last_executable) # type: ignore
        executable_with_actions = new_statement + self.actions
        executable_with_actions.append(executable)
    def retieve_program(self):
        return self.statements


class EvaluatorConfigs():
    pass

# develop further as game engine ?
class Evaluator():
    program: PROGRAM
    state_saver: int 
    logger: int
    transferable_checkpoint: Transformable
    def __init__(self, schema: ExecutionSchema, cfg: EvaluatorConfigs = EvaluatorConfigs()) -> None:
        self.schema = schema.retieve_program()
    def run(self, program_input: Input):
        # execution loop
        for i, st in enumerate(self.program):
            if i == 0:
                self.execute_input_statement(st, program_input)
            else:
                self.execute_ordinary_statement(st)
            print("Executed step: ", i)

    def execute_ordinary_statement(self, statement: STATEMENT):
        for el in statement:
            if  isinstance(el, Executable):
                self.transferable_checkpoint = el.execute(self.transferable_checkpoint, Transformable)
            else:
                Protocol.handle_transform(self.transferable_checkpoint, el)

    def execute_input_statement(self, statement: STATEMENT, input: Input):
        for i, el in enumerate(statement):
            if  isinstance(el, Executable):
                if i == 0:
                    self.transferable_checkpoint = el.execute(input, Transformable)
                else:
                    self.transferable_checkpoint = el.execute(self.transferable_checkpoint, Transformable)
            else:
                Protocol.handle_transform(self.transferable_checkpoint, el)





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




