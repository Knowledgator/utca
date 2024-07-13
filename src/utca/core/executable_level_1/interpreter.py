from __future__ import annotations
from typing import (
    Any, Dict, List, Optional, Tuple, Union, TYPE_CHECKING
)
import logging

from utca.core.executable_level_1.component import Component
from utca.core.executable_level_1.schema import Transformable
from utca.core.exceptions import EvaluatorExecutionFailed
if TYPE_CHECKING:
    from utca.core.executable_level_1.memory import MemoryManager


class Evaluator(Component):
    """
    Manages context of execution
    """
    memory_manager: MemoryManager
    schema: Component

    def __init__(
        self, 
        schema: Component, 
        logging_level: int=logging.NOTSET,
        logging_handler: Optional[logging.Handler]=None,
        fast_exit: bool=True,
        memory_manager: Optional[MemoryManager]=None,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            schema (Component): Wrapped Component.

            logging_level (int, optional): Logging level. Defaults to logging.NOTSET.
                See: https://docs.python.org/3/library/logging.html#logging-levels
            
            logging_handler (Optional[logging.Handler], optional): Handler that will be used.
                If value equals to None, default will be created. Defaults to None.
                See: https://docs.python.org/3/library/logging.html

            fast_exit (bool, optional): If set to True, after first unhandled exeception
                execution will be terminated. Defaults to True.
            
            memory_manager (Optional[MemoryManager], optional): Manages data, that can be accesed 
                in evaluator scope. If equals to None, default memory manager will be created.
                Defaults to None.

            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        from utca.core.executable_level_1.memory import MemoryManager
        super().__init__(name)
        self.logging_level = logging_level
        self.logging_handler = logging_handler or logging.StreamHandler()
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.logging_level)
        self.logger.addHandler(self.logging_handler)
        self.fast_exit = fast_exit
        self.memory_manager = memory_manager or MemoryManager()
        self.schema = schema


    def __call__(
        self, input_data: Transformable, evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        """
        Executes component with prepared data

        Args:
            input_data (Transformable): Data for processing

            evaluator (Optional[Evaluator], optional): Evaluator in context of which component executed.
                Defaults to None.

        Raises: 
            EvaluatorExecutionFailed: Reraised exception after logging to parent evaluator.        
        
        Returns:
            Transformable: Result of executed component.
        """
        try:
            return self.schema(input_data, self)
        except Exception as e:
            raise EvaluatorExecutionFailed(self.name, e)
        

    def run(
        self, input_data: Optional[Dict[str, Any]]=None, evaluator: Optional[Evaluator]=None
    ) -> Dict[str, Any]:
        """
        Run Component

        Args:
            input_data (Optional[Dict[str, Any]], optional): Data for processing. 
                If equals to None, empty dict will be used for input_data. Defaults to None.

            evaluator (Optional[Evaluator], optional): Evaluator in context of which component executed.
                Defaults to None.

        Returns:
            Dict[str, Any]: Result of execution.
        """
        return self(self.prepare_input(input_data), evaluator).extract()


    def get_memory(
        self, 
        register: Transformable, 
        identifiers: List[Union[str, Tuple[str, str]]],
        default: Dict[str, Any],
        delete: bool=False
    ) -> Transformable:
        """
        Get data from memory and set to register

        Args:
            register (Transformable): Destination.

            identifiers (List[Union[str, Tuple[str, str]]]): Key/keys that will be used to
                access data in memory and for setting to register.

            default (Dict[str, Any]): Returned value if keys not found. If equals to None, 
                an exception will be raised. Defaults to None.
            
            delete (bool, optional): If equals to True, accessed data will be removed from memory.
                Defaults to False.

        Returns:
            Transformable: Result of execution.
        """
        return self.memory_manager.get(
            register, identifiers, default, delete
        )

        
    def set_memory(
        self, 
        register: Transformable, 
        get_key: str,
        set_key: str,
    ) -> None:
        """
        Set data from register to memory

        Args:
            register (Transformable): Source.

            get_key (str): Key in register.
            
            set_key (str): Key in memory.
        """
        self.memory_manager.set(
            register, get_key, set_key
        )


    def delete_memory(
        self, identifier: str
    ) -> None:
        """
        Delete specified key from memory

        Args:
            identifier (str): Key for deletion.
        """
        self.memory_manager.delete(identifier)
        

    def flush_memory(self) -> None:
        """
        Delete all keys from memory
        """
        self.memory_manager.flush()
    

    def log(self, level: int, msg: Any, exc_info: bool=False) -> None:
        """
        Args:
            level (int): Logging level.

            msg (Any): Message to log.
            
            exc_info (bool, optional): Include exception info. Defaults to False.
        """
        self.logger.log(level, f"{self.name}: {msg}", exc_info=exc_info)

    
    def create_child(
        self, schema: Component, child_name: str
    ) -> Evaluator:
        """
        Create evaluator in context of current evaluator

        Args:
            schema (Component): Component to wrapp.

            child_name (str): Name of new evaluator.

        Returns:
            Evaluator: New evaluator.
        """
        return Evaluator(
            schema,
            name=f"{self.name}.{child_name}",
            logging_level=self.logging_level,
            logging_handler=self.logging_handler,
            fast_exit=self.fast_exit
        )
    

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.name} ({self.__dict__})"