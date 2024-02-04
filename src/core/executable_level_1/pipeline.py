

from typing import Union

from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import  Action, AddData, ChangeValue, ConfigType, InputType, MergeData, OutputType, RenameAttribute, RenameAttributeQuery, Transformable

# transformable can NOT be done on static fold
# how it can dynamic change ?
class Pipeline():

    def __ror__(self, __value: Union[Executable[ConfigType, InputType, OutputType], Transformable])-> int: 
        return 3
    
    def run(self) -> None:
        pass
    
    def run_protocol(self):
        pass

    def handle_transform(self, transform: Transformable, action: Action):
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



