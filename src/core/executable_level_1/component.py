from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.executable_level_1.statements_types import Statement
    from core.executable_level_1.eval import ExecutionSchema

class Component(ABC):
    def __or__(self, comp: Component) -> ExecutionSchema:
        from core.executable_level_1.eval import ExecutionSchema
        return ExecutionSchema(self).add(comp)


    @property
    @abstractmethod
    def statement(self) -> Statement:
        ...