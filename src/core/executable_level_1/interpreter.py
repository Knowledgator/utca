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
        self.name = name
        self.logging_level = logging_level
        self.logging_handler = logging_handler or logging.StreamHandler()
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.logging_level)
        self.logger.addHandler(self.logging_handler)
        self.fast_exit = fast_exit


class Evaluator:
    memory_manager: MemoryManager
    schema: Component
    cfg: EvaluatorConfigs

    def __init__(
        self, 
        schema: Component, 
        cfg: Optional[EvaluatorConfigs]=None,
        memory_manager: Optional[MemoryManager]=None,
    ) -> None:
        from core.executable_level_1.memory import MemoryManager
        self.cfg = cfg or EvaluatorConfigs()
        self.memory_manager = memory_manager or MemoryManager()
        self.schema = schema


    def prepare_input(
        self, 
        input_data: Optional[Dict[str, Any]]=None
    ) -> Transformable:
        """Sets the initial input for the program."""
        if input_data is not None:
            return Transformable(input_data)
        return Transformable({})


    def run(
        self, input_data: Optional[Dict[str, Any]]=None
    ) -> Dict[str, Any]:    
        return self.eval(self.prepare_input(input_data)).extract()
    

    def eval(self, input_data: Transformable) -> Transformable:
        return self.schema(input_data, self)

    
    def get_memory(
        self, 
        register: Transformable, 
        identifiers: List[Union[str, Tuple[str, str]]],
        delete: bool=False
    ) -> Transformable:
        return self.memory_manager.get(
            register, identifiers, delete
        )

        
    def set_memory(
        self, 
        register: Transformable, 
        get_key: str,
        set_key: str,
    ) -> None:
        self.memory_manager.set(
            register, get_key, set_key
        )


    def delete_memory(
        self, identifier: str
    ) -> None:
        self.memory_manager.delete(identifier)
        

    def flush_memory(self) -> None:
        self.memory_manager.flush()
    

    def log(self, level: int, msg: Any, exc_info: bool=False) -> None:
        self.cfg.logger.log(level, f"{self.cfg.name}: {msg}", exc_info=exc_info)

    
    def create_child(
        self, schema: Component, child_name: str
    ) -> Evaluator:
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