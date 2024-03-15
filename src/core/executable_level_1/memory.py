import os
import json
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from core.executable_level_1.component import Component
from core.executable_level_1.schema import Transformable
from core.executable_level_1.statements_types import Statement

INPUT: str = 'input'

class Memory:
    memory: Dict[str, Any]
    def __init__(self, directory: Optional[str] = None) -> None:
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
        return None  # Return None if the state is not found


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


class MemorySetInstruction(Enum):
    SET_AND_GO = "setandgo" # set and continue
    SET_AND_FLUSH = "setandflush" # clean all objects
    FLUSH = "flush"

    # FLUSH_AND_RESTORE_INPUT = "restoreinput" # clean all objects + set initial input state




class SetMemory(Component):
    identifier: str
    memory_instruction: MemorySetInstruction

    def __init__(
        self, 
        identifier: str,
        memory_instruction: MemorySetInstruction=MemorySetInstruction.SET_AND_GO,
    ) -> None:
        super().__init__()
        self.identifier = identifier
        self.memory_instruction = memory_instruction


    def get_identifier(self):
        return self.identifier
    
    
    def get_memory_instruction(self):
        return self.memory_instruction
    

    @property
    def statement(self) -> Statement:
        return Statement.SET_MEMORY_STATEMENT


class MemoryGetInstruction(Enum):
    GET_AND_GO = "getandgo" # get and merge
    FLUSH_AND_GET = "flushandget" # clean all objects and get


class GetMemory(Component):
    identifiers: List[str]
    memory_instruction: MemoryGetInstruction

    def __init__(
        self, 
        identifiers: List[str],
        memory_instruction: MemoryGetInstruction=MemoryGetInstruction.GET_AND_GO,
    ):
        super().__init__()
        self.identifiers = identifiers
        self.memory_instruction = memory_instruction

    
    def get_identifiers(self) -> List[str]:
        return self.identifiers
    
    
    def get_memory_instruction(self) -> MemoryGetInstruction:
        return self.memory_instruction
    

    @property
    def statement(self) -> Statement:
        return Statement.GET_MEMORY_STATEMENT
    

class MemoryManager():
    memory: Memory
    def __init__(self, path: Optional[str]) -> None:
        if path:
            self.memory = Memory(path)
        else:
            self.memory = Memory()


    def resolve_get_memory(self, command: GetMemory, register: Transformable):
        instr = command.get_memory_instruction()
        identifiers = command.get_identifiers()
        if instr == MemoryGetInstruction.GET_AND_GO:
            register = self.get_and_go(register, identifiers)
        elif  instr == MemoryGetInstruction.FLUSH_AND_GET: 
            register = self.flush_and_get(identifiers)
        return register

        
    def get_and_go(
        self, 
        register: Transformable, 
        identifiers: List[str],
    ) -> Transformable:
        for identifier in identifiers:
            setattr(
                register,
                identifier,
                self.memory.retrieve_store(identifier)
            )
        return register
    

    def flush_and_get(self, identifiers: List[str]) -> Transformable:
        return self.get_and_go(Transformable({}), identifiers)


     # set memory commands

    def resolve_set_memory(self, command: SetMemory, register: Transformable):
        ## TODO: refactor redundant transformable and dict transversion
        registerDict = register.extract()
        instr = command.get_memory_instruction()
        identifiers = command.get_identifier()

        if instr == MemorySetInstruction.SET_AND_GO:
            self.set_and_go(registerDict, identifiers)
        elif  instr == MemorySetInstruction.SET_AND_FLUSH: 
            registerDict = self.set_and_flush(registerDict, identifiers)
        elif instr == MemorySetInstruction.FLUSH:
            registerDict = self.flush()
        return Transformable(registerDict)

    
    def set_and_go(
        self, 
        register: Union[Dict[str, Any], List[Dict[str, Any]]], 
        identifier: str
    ):
        self.memory.add_store(identifier, register)
    
    
    def set_and_flush(
        self, 
        register: Union[Dict[str, Any], List[Dict[str, Any]]], 
        identifier: str
    ) -> Dict[str, Any]:
        self.set_and_go(register, identifier)
        return {}
    
    
    def flush(self) -> Dict[str, Any]:
        return {}