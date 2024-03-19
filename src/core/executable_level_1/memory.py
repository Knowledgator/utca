import os
import json
from enum import Enum
from typing import (
    Any, Dict, List, Optional, Tuple, Union
)

from core.executable_level_1.component import Component
from core.executable_level_1.schema import Transformable
from core.executable_level_1.statements_types import Statement

INPUT: str = 'input'

class Memory:
    memory: Dict[str, Any]

    def __init__(self, directory: Optional[str]=None) -> None:
        self.memory = {}
        self.directory = directory
        if directory:
            os.makedirs(directory, exist_ok=True)


    # def add_input(self, input_state: Dict[str, Any]):
    #     self.add_store(INPUT, input_state)
            

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
    
    
    def get_memory_instruction(self):
        return self.memory_instruction
    

    @property
    def statement(self) -> Statement:
        return Statement.SET_MEMORY_STATEMENT


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

    
    def get_identifiers(self) -> List[Union[str, Tuple[str, str]]]:
        return self.identifiers
    
    
    def get_memory_instruction(self) -> MemoryGetInstruction:
        return self.memory_instruction
    

    @property
    def statement(self) -> Statement:
        return Statement.GET_MEMORY_STATEMENT


class DeleteMemory(Component):
    def __init__(
        self, identifiers: Optional[List[str]]=None,
    ):
        self.identifiers = identifiers


    @property
    def statement(self) -> Statement:
        return Statement.DELETE_MEMORY_STATEMENT


    def get_identifiers(self) -> Optional[List[str]]:
        return self.identifiers


class MemoryManager:
    memory: Memory

    def __init__(self, path: Optional[str]=None) -> None:
        if path:
            self.memory = Memory(path)
        else:
            self.memory = Memory()


    def resolve_get_memory(
        self, 
        command: GetMemory, 
        register: Transformable
    ) -> Transformable:
        instr = command.get_memory_instruction()
        identifiers = command.get_identifiers()
        if instr == MemoryGetInstruction.GET:
            register = self.get(register, identifiers)
        elif instr == MemoryGetInstruction.REPLACE: 
            register = self.get(Transformable({}), identifiers)
        elif instr == MemoryGetInstruction.POP:
            register = self.get(register, identifiers, delete=True)
        return register

        
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


    def resolve_set_memory(
        self, command: SetMemory, register: Transformable
    ) -> Transformable:
        instr = command.get_memory_instruction()

        if instr == MemorySetInstruction.SET:
            self.set(
                register, command.get_key, command.set_key
            )
        elif  instr == MemorySetInstruction.MOVE: 
            self.set(
                register, command.get_key, command.set_key
            )
            if command.get_key == "__dict__":
                register.flush()
            else:
                delattr(register, command.get_key) 
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

    
    def resolve_delete_memory(
        self, 
        command: DeleteMemory, 
    ) -> None:
        identifiers = command.get_identifiers()
        if not identifiers:
            return self.memory.flush()
        for i in identifiers:
            self.memory.delete_store(i)