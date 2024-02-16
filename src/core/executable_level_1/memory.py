
from enum import Enum
from typing import Any, Dict, List, Optional

from core.executable_level_1.component import Component

INPUT: str = 'input'


import os
import json

class Memory:
    memory: Dict[str, Any]
    def __init__(self, directory: Optional[str] = None) -> None:
        self.memory = {}
        self.directory = directory
        if directory:
            os.makedirs(directory, exist_ok=True)

    def add_input(self, input_state: Dict[str, Any]):
        self.add_store(INPUT, input_state)
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
    FLUSH = "flush" # clean all objects
    FLUSH_AND_RESTORE_INPUT = "restoreinput" # clean all objects + set initial input state
    FLUSH_AND_GET_STATE = "flushandgetstate" # clean and set other state
    FLUSH_AND_GET_MP_STATE = "flushandgetmpstate" # clean and get many merged states



class SetMemory(Component):
    set_name: str
    memory_instruction: Optional[MemorySetInstruction]
    get_states: Optional[List[str]]
    def __init__(self, set_name: str,
                 memory_instruction: Optional[MemorySetInstruction] = MemorySetInstruction.SET_AND_GO,
                 get_states: Optional[List[str]] = None) -> None:
        super().__init__()
        self.set_name = set_name
        self.memory_instruction = memory_instruction
        self.get_states = get_states if get_states is not None else []




class MemoryGetInstruction(Enum):
    GET_AND_GO = "getandgo" # get and merge
    FLUSH_AND_GET = "flushandget" # clean all objects and get
    MP_GET_AND_GO = "mpgetandgo" # mp get and merge
    FLUSH_AND_MP_GET = "flushandmpget" # clean all objects and mp get


class GetMemory(Component):
    get_name: List[str]
    memory_instruction: Optional[MemoryGetInstruction]
    def __init__(self, get_name: List[str],
                 memory_instruction: Optional[MemoryGetInstruction] = MemoryGetInstruction.GET_AND_GO):
        super().__init__()
        self.get_name = get_name
        self.memory_instruction = memory_instruction
