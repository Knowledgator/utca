from typing import  Optional, Union, List

from core.executable_level_1.component import Component
from core.executable_level_1.custom_exceptions import ExecutionSchemaInvalidFirstComponent

from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import  Action, AddData, ChangeValue, Config, ConfigType, Input, InputType, MergeData, Output, OutputType, RenameAttribute, RenameAttributeQuery, Transformable


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

# develop further as game engine ?
class Evaluator():
    program: PROGRAM
    state_saver: int 
    logger: int
    def __init__(self, schema: ExecutionSchema) -> None:
        self.schema = schema.retieve_program()
    def run(self):
        # execution loop
        for i, st in enumerate(self.program):
            self.execute_statement(st)
            print("Executed step: ", i)
    def execute_statement(self, statement: STATEMENT):
        for el in statement:
            if el is Executable:
                pass
            else:
                pass





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




