from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Union

from core.executable_level_1.statements_types import Statement
if TYPE_CHECKING:
    from core.executable_level_1.eval import ExecutionSchema  # Forward declaration for type checking

class Component(ABC):
    def __or__(self, comp: Component) -> ExecutionSchema:
        from core.executable_level_1.eval import ExecutionSchema
        return ExecutionSchema(self).add(comp)
    
    
    def __ror__(self, comp: Union[ExecutionSchema, Component]) -> ExecutionSchema:
        from core.executable_level_1.eval import ExecutionSchema
        if isinstance(comp, ExecutionSchema):
            return comp.add(self)
        else:
            return ExecutionSchema(comp).add(self)


    @abstractmethod
    def generate_statement(self) -> Dict[Statement, Any]:
        ...

