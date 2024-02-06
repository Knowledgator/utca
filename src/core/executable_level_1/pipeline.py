from typing import Any, Union, List
from core.executable_level_1.component import Component

from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import  Action, AddData, ChangeValue, Config, ConfigType, Input, InputType, MergeData, Output, OutputType, RenameAttribute, RenameAttributeQuery, Transformable


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
    last_executable: Executable[Config, Input, Output]
    transformer: Transformable
    statements: List[Union[List[Executable[Config, Input, Output]], List[Action]]]
    def __init__(self, component: Component) -> None:
        if component is Executable[Config, Input, Output]:
            self.last_executable = component

    def add(self, comp: Component):
        pass


class Evaluator():
    pass





# transformable can NOT be done on static fold
# how it can dynamic change ?

# Головні питання:
#  чи наслідується від executable ? + є io + спільний метода і передача
# 
# 
class Pipeline():
    last_exec: Executable[Config, Input, Output]
    def __ror__(self, __value: Union[Executable[ConfigType, InputType, OutputType], Transformable])-> int:
        # add 2 pipelines
        return 3
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass
    def run(self) -> None:
        pass
    
    def run_protocol(self):

        pass




