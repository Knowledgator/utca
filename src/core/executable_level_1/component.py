from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TYPE_CHECKING
# from enum import Enum

if TYPE_CHECKING:
    from core.executable_level_1.schema import Transformable
    from core.executable_level_1.eval import ExecutionSchema  # Forward declaration for type checking

class Component(ABC):
    @abstractmethod
    def __call__(
        self, 
        register: Transformable, 
        set_key: Optional[str]=None,
        get_key: Optional[str]=None,
    ) -> Transformable:
        ...


    def __or__(self, comp: Component) -> ExecutionSchema:
        from core.executable_level_1.eval import ExecutionSchema
        return ExecutionSchema(self).add(comp)


    @abstractmethod
    def generate_statement(self) -> Dict[str, Any]:
        ...

    
class Executor(Component):
    component: Component
    get_key: Optional[str]
    set_key: Optional[str]
    
    def __init__(
        self, 
        component: Component,
        get_key: Optional[str]=None,
        set_key: Optional[str]=None
    ) -> None:
        self.component = component
        self.get_key = get_key
        self.set_key = set_key

    
    def __call__(
        self, 
        register: Transformable, 
        get_key: Optional[str]=None,
        set_key: Optional[str]=None,
    ) -> Transformable:
        logging.error(f"{self.set_key} - {self.get_key}")
        return self.component(
            register=register,
            get_key=get_key or self.get_key,
            set_key=set_key or self.set_key
        )


    def generate_statement(self) -> Dict[str, Any]:
        return self.component.generate_statement()