from __future__ import annotations
from typing import (
    Dict, Any, List, Optional, Tuple, Union, TYPE_CHECKING
)
import logging

from core.executable_level_1.component import Component
from core.executable_level_1.schema import Transformable
if TYPE_CHECKING:
    from core.executable_level_1.memory import MemoryManager

INPUT = "input"

class EvaluatorConfigs:
    """
    Configuration for evaluator
    """
    logging_level: int
    logging_handler: logging.Handler
    logger: logging.Logger
    fast_exit: bool

    def __init__(
        self,
        name: str="Evaluator", 
        logging_level: int=logging.NOTSET,
        logging_handler: Optional[logging.Handler]=None,
        fast_exit: bool=True
    ):
        """
        Args:
            name (str, optional): Identification name. Defaults to "Evaluator".
            
            logging_level (int, optional): Logging level. Defaults to logging.NOTSET.
            
            logging_handler (Optional[logging.Handler], optional): Handler that will be used.
                Defaults to None.

            fast_exit (bool, optional): If set to True, after first unhandled exeception
                execution will be terminated. Defaults to True.

        """
        self.name = name
        self.logging_level = logging_level
        self.logging_handler = logging_handler or logging.StreamHandler()
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.logging_level)
        self.logger.addHandler(self.logging_handler)
        self.fast_exit = fast_exit


class Evaluator:
    """
    Manages context of execution
    """
    memory_manager: MemoryManager
    schema: Component
    cfg: EvaluatorConfigs

    def __init__(
        self, 
        schema: Component, 
        cfg: Optional[EvaluatorConfigs]=None,
        memory_manager: Optional[MemoryManager]=None,
    ) -> None:
        """
        Args:
            schema (Component): Wrapped Component.

            cfg (Optional[EvaluatorConfigs], optional): Evaluator configuration.
                If value equals to None, default configuration will be created. 
                Defaults to None.
            
            memory_manager (Optional[MemoryManager], optional): Manages data, that can be accesed 
                in evaluator scope. If equals to None, default memory manager will be created.
                Defaults to None.
        """
        from core.executable_level_1.memory import MemoryManager
        self.cfg = cfg or EvaluatorConfigs()
        self.memory_manager = memory_manager or MemoryManager()
        self.schema = schema


    def prepare_input(
        self, 
        input_data: Optional[Dict[str, Any]]=None
    ) -> Transformable:
        """
        Sets the initial input for the program.

        Args:
            input_data (Optional[Dict[str, Any]], optional): Initial data. Defaults to None.

        Returns:
            Transformable: Prepared data.
        """
        if input_data is not None:
            return Transformable(input_data)
        return Transformable({})


    def run(
        self, input_data: Optional[Dict[str, Any]]=None
    ) -> Dict[str, Any]:
        """
        Execution of wrapped component

        Args:
            input_data (Optional[Dict[str, Any]], optional): Data for processing. 
                Defaults to None.

        Returns:
            Dict[str, Any]: Result of execution.
        """
        return self.eval(self.prepare_input(input_data)).extract()
    

    def eval(self, input_data: Transformable) -> Transformable:
        """
        Executes component with prepared data

        Args:
            input_data (Transformable): Prepared data.

        Returns:
            Transformable: Result of execution.
        """
        return self.schema(input_data, self)

    
    def get_memory(
        self, 
        register: Transformable, 
        identifiers: List[Union[str, Tuple[str, str]]],
        delete: bool=False
    ) -> Transformable:
        """
        Add data from memory to register

        Args:
            register (Transformable): Destination.

            identifiers (List[Union[str, Tuple[str, str]]]): Key/keys that will be used to
                access data in memory and for setting to register.
            
            delete (bool, optional): If equals to True, accessed data will be removed from memory.
                Defaults to False.

        Returns:
            Transformable: Result of execution.
        """
        return self.memory_manager.get(
            register, identifiers, delete
        )

        
    def set_memory(
        self, 
        register: Transformable, 
        get_key: str,
        set_key: str,
    ) -> None:
        """
        Sets data from register to memory

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
        Deletes specified key from memory

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
        self.cfg.logger.log(level, f"{self.cfg.name}: {msg}", exc_info=exc_info)

    
    def create_child(
        self, schema: Component, child_name: str
    ) -> Evaluator:
        """
        Creates evaluator in context of current evaluator

        Args:
            schema (Component): Component to wrapp.

            child_name (str): Name of new evaluator.

        Returns:
            Evaluator: New evaluator.
        """
        return Evaluator(
            schema,
            cfg=EvaluatorConfigs(
                name=f"{self.cfg.name}.{child_name}",
                logging_level=self.cfg.logging_level,
                logging_handler=self.cfg.logging_handler,
                fast_exit=self.cfg.fast_exit
            )
        )
    

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.cfg.name} ({self.__dict__})"