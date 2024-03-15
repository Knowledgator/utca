from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING, Union
# from enum import Enum

if TYPE_CHECKING:
    from core.executable_level_1.schema import Transformable, InputType, OutputType
    from core.executable_level_1.statements_types import Statement
    from core.executable_level_1.executable import Executable
    from core.executable_level_1.actions import Action, ActionInput, ActionOutput
    from core.executable_level_1.eval import ExecutionSchema  # Forward declaration for type checking

class Component(ABC):
    # @abstractmethod
    # def __call__(
    #     self, 
    #     register: Transformable, 
    #     set_key: Optional[str]=None,
    #     get_key: Optional[str]=None,
    # ) -> Transformable:
    #     ...


    def __or__(self, comp: Component) -> ExecutionSchema:
        from core.executable_level_1.eval import ExecutionSchema
        return ExecutionSchema(self).add(comp)


    @property
    @abstractmethod
    def statement(self) -> Statement:
        ...

    
class Executor(Component):
    def __init__(
        self, 
        component: Union[
            Action[ActionInput, ActionOutput], 
            Executable[InputType, OutputType]
        ],
        get_key: Optional[str]=None,
        set_key: Optional[str]=None
    ) -> None:
        self.component = component
        self.get_key = get_key
        self.set_key = set_key

    
    def __call__(
        self, 
        register: Transformable,
    ) -> Transformable:
        return self.component(
            register, self.get_key, self.set_key
        )


    @property
    def statement(self) -> Statement:
        return self.component.statement