from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, TYPE_CHECKING
# from enum import Enum

from core.executable_level_1.schema import (
    Config
)
from core.executable_level_1.statements_types import Statement
if TYPE_CHECKING:
    from core.executable_level_1.eval import Pipeline  # Forward declaration for type checking

class Component(ABC):
    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg


    def __or__(self, comp: Component) -> Pipeline:
        from core.executable_level_1.eval import Pipeline
        return Pipeline(None, self).add(comp)


    @abstractmethod
    def execute(
        self, input_data: Any
    ) -> Any:
        ...


    @abstractmethod
    def execute_batch(
        self, input_data: List[Any], 
    ) -> Any:
        ...


    @abstractmethod
    def generate_statement(self) -> Dict[Statement, Any]:
        ...