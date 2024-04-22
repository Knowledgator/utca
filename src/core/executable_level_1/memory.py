from __future__ import annotations
import os
import json
from enum import Enum
from typing import (
    Any, Dict, List, Optional, Tuple, Union
)

from core.executable_level_1.component import Component
from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.schema import Transformable
from core.exceptions import InavalidMemoryInstruction

class Memory:
    memory: Dict[str, Any]

    def __init__(
        self, 
        directory: Optional[str]=None, 
        initial_data: Optional[Dict[str, Any]]=None
    ) -> None:
        self.memory = initial_data or {}
        self.directory = directory
        if directory:
            os.makedirs(directory, exist_ok=True)
            

    def _get_file_path(self, identifier: str) -> str:
        """Constructs a file path for a given identifier."""
        if not self.directory:
            raise ValueError("No directory set for file-based storage.")
        return os.path.join(self.directory, f"{identifier}.json")


    def add_store(self, identifier: str, state: Any) -> None:
        """Saves a state with the given identifier."""
        self.memory[identifier] = state
        if self.directory:
            file_path = self._get_file_path(identifier)
            with open(file_path, 'w') as f:
                json.dump(state, f)


    def retrieve_store(self, identifier: str) -> Any:
        """Retrieves a state by its identifier, either from memory or disk."""
        if identifier in self.memory:
            return self.memory[identifier]
        if self.directory:
            file_path = self._get_file_path(identifier)
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
        raise KeyError(f"No specified identifier found: {identifier}")


    def delete_store(self, identifier: str) -> None:
        """Deletes a state by its identifier from both memory and disk."""
        # Remove from memory
        if identifier in self.memory:
            del self.memory[identifier]
        
        # Remove from disk if applicable
        if self.directory:
            file_path = self._get_file_path(identifier)
            if os.path.exists(file_path):
                os.remove(file_path)
    

    def flush(self) -> None:
        self.memory = {}


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"


class MemorySetInstruction(Enum):
    SET = "setandgo" # set and continue
    MOVE = "move" # clean all objects
    # FLUSH_AND_RESTORE_INPUT = "restoreinput" # clean all objects + set initial input state


class SetMemory(Component):
    get_key: str
    set_key: str
    memory_instruction: MemorySetInstruction

    def __init__(
        self, 
        set_key: str,
        get_key: Optional[str]=None,
        memory_instruction: MemorySetInstruction=MemorySetInstruction.SET,
    ) -> None:
        super().__init__()
        self.set_key = set_key
        self.get_key = get_key or "__dict__"
        self.memory_instruction = memory_instruction


    def __call__(
        self, input_data: Transformable, evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        if not evaluator:
            evaluator = self.set_up_default_evaluator()
        
        evaluator.set_memory(
            input_data, self.get_key, self.set_key
        )
        if self.memory_instruction == MemorySetInstruction.SET:
            return input_data
        elif self.memory_instruction == MemorySetInstruction.MOVE: 
            if self.get_key == "__dict__":
                input_data.flush()
            else:
                delattr(input_data, self.get_key)
        else:
            raise InavalidMemoryInstruction() 
        return input_data


class MemoryGetInstruction(Enum):
    GET = "get" # get and merge
    REPLACE = "replace" # clean all objects and get
    POP = "pop"


class GetMemory(Component):
    identifiers: List[Union[str, Tuple[str, str]]]
    memory_instruction: MemoryGetInstruction

    def __init__(
        self, 
        identifiers: List[Union[str, Tuple[str, str]]],
        memory_instruction: MemoryGetInstruction=MemoryGetInstruction.GET,
    ):
        super().__init__()
        self.identifiers = identifiers
        self.memory_instruction = memory_instruction

    
    def __call__(
        self, input_data: Transformable, evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        if not evaluator:
            evaluator = self.set_up_default_evaluator()

        if self.memory_instruction == MemoryGetInstruction.GET:
            register = evaluator.get_memory(input_data, self.identifiers)
        elif self.memory_instruction == MemoryGetInstruction.REPLACE: 
            register = evaluator.get_memory(Transformable(), self.identifiers)
        elif self.memory_instruction == MemoryGetInstruction.POP:
            register = evaluator.get_memory(input_data, self.identifiers, delete=True)
        else:
            raise InavalidMemoryInstruction()
        return register


class DeleteMemory(Component):
    def __init__(
        self, identifiers: Optional[List[str]]=None,
    ):
        self.identifiers = identifiers


    def execute(
        self, register: Transformable, memory_manager: MemoryManager
    ) -> Transformable:
        if not self.identifiers:
            memory_manager.flush()
        else:
            for i in self.identifiers:
                memory_manager.delete(i)
        return register


class MemoryManager:
    memory: Memory

    def __init__(
        self, 
        path: Optional[str]=None, 
        initial_data: Optional[Dict[str, Any]]=None
    ) -> None:
        self.memory = Memory(path, initial_data)

        
    def get(
        self, 
        register: Transformable, 
        identifiers: List[Union[str, Tuple[str, str]]],
        delete: bool=False
    ) -> Transformable:
        for identifier in identifiers:
            if isinstance(identifier, tuple):
                get_key = identifier[0]
                set_key = identifier[1]
            else:
                get_key = identifier
                set_key = identifier
            setattr(
                register,
                set_key,
                self.memory.retrieve_store(get_key)
            )
            if delete: # need refactor!
                self.memory.delete_store(get_key)
        return register

        
    def set(
        self, 
        register: Transformable, 
        get_key: str,
        set_key: str,
    ):
        self.memory.add_store(
            set_key, getattr(register, get_key)
        )


    def delete(
        self, identifier: str
    ) -> None:
        self.memory.delete_store(identifier)
        

    def flush(self) -> None:
        self.memory.flush()


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"