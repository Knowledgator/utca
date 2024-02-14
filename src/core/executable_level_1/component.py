from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Union

if TYPE_CHECKING:
    from core.executable_level_1.eval import ExecutionSchema  # Forward declaration for type checking

class Component(ABC):
    def __or__(self, comp: Component) -> ExecutionSchema:
        from core.executable_level_1.eval import ExecutionSchema
        if isinstance(self, ExecutionSchema):
            self.add(comp)
            return self
        else:
            e = ExecutionSchema(self)
            e.add(comp)
            return e
    
    
    def __ror__(self, comp: Union[ExecutionSchema, Component]) -> ExecutionSchema:
        from core.executable_level_1.eval import ExecutionSchema
        if isinstance(comp, ExecutionSchema):
            comp.add(self)
            return comp
        else:
            e = ExecutionSchema(comp)
            e.add(self)
            return e

    @abstractmethod
    def generate_statement(self) -> Dict[str, Any]:
        pass

