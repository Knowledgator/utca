from typing import (
    Any, Generic, Optional, TypeVar,
)

from core.executable_level_1.executable import Executable
from core.executable_level_1.actions import Action
from core.executable_level_1.component import Component
from core.executable_level_1.schema import Transformable
from core.executable_level_1.statements_types import Statement

EvalStatement = TypeVar("EvalStatement", Action[Any, Any], Executable[Any, Any])

class Executor(Component, Generic[EvalStatement]):
    def __init__(
        self, 
        component: EvalStatement, 
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