from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TYPE_CHECKING

from core.executable_level_1.schema import Transformable
if TYPE_CHECKING:
    from core.executable_level_1.eval import ExecutionSchema
    from core.executable_level_1.interpreter import Evaluator

class Component(ABC):
    def __init__(self, name: Optional[str]=None):
        self._name = name or self.__class__.__name__


    def __or__(self, comp: Component) -> ExecutionSchema:
        from core.executable_level_1.eval import ExecutionSchema
        return ExecutionSchema(self).add(comp)


    def set_up_default_evaluator(self) -> Evaluator:
        from core.executable_level_1.interpreter import Evaluator
        return Evaluator(self)


    @abstractmethod
    def __call__(
        self, input_data: Transformable, evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        ...


    def prepare_input(
        self, input_data: Optional[Dict[str, Any]]=None
    ) -> Transformable:
        """Sets the initial input for the program."""
        if input_data is not None:
            return Transformable(input_data)
        return Transformable({})


    def run(
        self, input_data: Optional[Dict[str, Any]]=None
    ) -> Dict[str, Any]:    
        return self(self.prepare_input(input_data)).extract()

    
    @property
    def name(self) -> str:
        return self._name
    

    def set_name(self, name: str) -> Component:
        self._name = name
        return self
    

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.name} ({self.__dict__})"