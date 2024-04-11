from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.executable_level_1.eval import ExecutionSchema
    from core.executable_level_1.interpreter import Evaluator
    from core.executable_level_1.schema import Transformable

class Component(ABC):
    def __or__(self, comp: Component) -> ExecutionSchema:
        from core.executable_level_1.eval import ExecutionSchema
        return ExecutionSchema(self).add(comp)


    @abstractmethod
    def __call__(
        self, input_data: Transformable, evaluator: Evaluator
    ) -> Transformable:
        ...