from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TYPE_CHECKING
# from enum import Enum

from core.executable_level_1.schema import (
    Config
)
if TYPE_CHECKING:
    from core.executable_level_1.eval import ExecutionSchema  # Forward declaration for type checking

class Component(ABC):
    def __init__(self, cfg: Optional[Config] = None) -> None:
        self.cfg = cfg or Config()


    def __or__(self, comp: Component) -> ExecutionSchema:
        from core.executable_level_1.eval import ExecutionSchema
        return ExecutionSchema(self).add(comp)


    @abstractmethod
    def generate_statement(self) -> Dict[str, Any]:
        ...