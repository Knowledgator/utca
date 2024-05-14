from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TYPE_CHECKING

from utca.core.executable_level_1.schema import Transformable
if TYPE_CHECKING:
    from utca.core.executable_level_1.eval import ExecutionSchema
    from utca.core.executable_level_1.interpreter import Evaluator

class Component(ABC):
    """
    The base class for the main components of UTCA programs
    """
    def __init__(self, name: Optional[str]=None):
        """
        Args:
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        self._name = name or self.__class__.__name__


    def __or__(self, component: Component) -> ExecutionSchema:
        """
        Create ExecutionSchema from two components

        Args:
            component (Component): Component that will be added 
                with this component to ExecutionSchema.

        Returns:
            ExecutionSchema: Result of combination of two components.
                When schema will be called, this component will be executed first.
        """
        from utca.core.executable_level_1.eval import ExecutionSchema
        return ExecutionSchema(self).add(component)


    def set_up_default_evaluator(self) -> Evaluator:
        """
        Creates default Evaluator.

        Returns:
            Evaluator: Evaluator that will be used as a context 
                of execution of this component.
        """
        from utca.core.executable_level_1.interpreter import Evaluator
        return Evaluator(self)


    @abstractmethod
    def __call__(
        self, input_data: Transformable, evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        """
        Component Call

        Args:
            input_data (Transformable): Data for processing

            evaluator (Optional[Evaluator], optional): Evaluator in context of which component executed.
                If equals to None, default evaluator will be created. Defaults to None.

        Returns:
            Transformable: Result of executed component.
        """
        ...


    def prepare_input(
        self, input_data: Optional[Dict[str, Any]]=None
    ) -> Transformable:
        """
        Sets the initial input for the program.

        Args:
            input_data (Optional[Dict[str, Any]], optional): Data for processing. 
                If equals to None, empty dict will be used for input_data. Defaults to None.

        Returns:
            Transformable: Initial input.
        """
        if input_data is not None:
            return Transformable(input_data)
        return Transformable({})


    def run(
        self, input_data: Optional[Dict[str, Any]]=None, evaluator: Optional[Evaluator]=None
    ) -> Dict[str, Any]:
        """
        Run Component

        Args:
            input_data (Optional[Dict[str, Any]], optional): Data for processing. 
                If equals to None, empty dict will be used for input_data. Defaults to None.

            evaluator (Optional[Evaluator], optional): Evaluator in context of which component executed.
                If equals to None, default evaluator will be created. Defaults to None.

        Returns:
            Dict[str, Any]: Result of execution.
        """
        return self(self.prepare_input(input_data), evaluator).extract()

    
    @property
    def name(self) -> str:
        """
        Name for identification
        """
        return self._name
    

    def set_name(self, name: str) -> Component:
        """
        Args:
            name (str): New name.

        Returns:
            Component: self
        """
        self._name = name
        return self
    

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.name} ({self.__dict__})"