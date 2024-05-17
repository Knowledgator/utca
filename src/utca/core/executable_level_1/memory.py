from __future__ import annotations
import os
import json
from enum import Enum
from typing import (
    Any, Dict, List, Optional, Tuple, Union
)

from utca.core.executable_level_1.component import Component
from utca.core.executable_level_1.interpreter import Evaluator
from utca.core.executable_level_1.schema import Transformable
from utca.core.exceptions import InavalidMemoryInstruction

class Memory:
    """
    Manage data
    """
    memory: Dict[str, Any]

    def __init__(
        self, 
        directory: Optional[str]=None, 
        initial_data: Optional[Dict[str, Any]]=None
    ) -> None:
        """
        Args:
            directory (Optional[str], optional): Path to directory. Defaults to None.
            
            initial_data (Optional[Dict[str, Any]], optional): Data for initialization 
                of memory. Defaults to None.
        """
        self.memory = initial_data or {}
        self.directory = directory
        if directory:
            os.makedirs(directory, exist_ok=True)
            

    def _get_file_path(self, identifier: str) -> str:
        """
        Construct a file path for a given identifier

        Args:
            identifier (str): Indetifier that will be used.

        Raises:
            ValueError: If directory was not specified.

        Returns:
            str: Path to file for identifier.
        """
        if not self.directory:
            raise ValueError("No directory set for file-based storage.")
        return os.path.join(self.directory, f"{identifier}.json")


    def add_store(self, identifier: str, state: Any) -> None:
        """
        Save state with the given identifier

        Args:
            identifier (str): Identifier that will be used.

            state (Any): State that will be associated with provided identifier.
        """
        self.memory[identifier] = state
        if self.directory:
            file_path = self._get_file_path(identifier)
            with open(file_path, 'w') as f:
                json.dump(state, f)


    def retrieve_store(self, identifier: str) -> Any:
        """
        Retrieve state by its identifier, either from memory or disk

        Args:
            identifier (str): Identifier that will be used.

        Raises:
            KeyError: If identiifier is invalid.

        Returns:
            Any: Data associated with identifier.
        """
        if identifier in self.memory:
            return self.memory[identifier]
        if self.directory:
            file_path = self._get_file_path(identifier)
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
        raise KeyError(f"No specified identifier found: {identifier}")


    def delete_store(self, identifier: str) -> None:
        """
        Delete a state by its identifier from both memory and disk

        Args:
            identifier (str): Identifier to delete.
        """
        # Remove from memory
        if identifier in self.memory:
            del self.memory[identifier]
        
        # Remove from disk if applicable
        if self.directory:
            file_path = self._get_file_path(identifier)
            if os.path.exists(file_path):
                os.remove(file_path)
    

    def flush(self) -> None:
        """
        Clean memory
        """
        self.memory = {}


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"


class MemorySetInstruction(Enum):
    """
    Set memory instruction
    """
    SET = 0
    """
    Set data to memory
    """
    MOVE = 1
    """
    Set data to memory and remove it from current data
    """
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
        """
        Args:
            set_key (str): Destination key.

            get_key (Optional[str], optional): Key that used to retrieve data from register. 
                If equals to None, complete register will be added to memory. Defaults to None.
            
            memory_instruction (MemorySetInstruction, optional): Strategy for memory setting.
                Defaults to MemorySetInstruction.SET.
        """
        super().__init__()
        self.set_key = set_key
        self.get_key = get_key or "__dict__"
        self.memory_instruction = memory_instruction


    def __call__(
        self, input_data: Transformable, evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        """
        Args:
            input_data (Transformable): Current data.
            
            evaluator (Optional[Evaluator], optional): Evaluator in context of which executed.
                If equals to None, default evaluator will be created. Defaults to None.

        Raises:
            InavalidMemoryInstruction: If provided instruction doesnt exists.

        Returns:
            Transformable: Result of execution.
        """
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
            return input_data
        else:
            raise InavalidMemoryInstruction() 


class MemoryGetInstruction(Enum):
    """
    Get memory instruction
    """
    GET = 0
    """
    Get data from memory
    """
    POP = 1
    """
    Get data from memory and delete it from memory
    """


class GetMemory(Component):
    identifiers: List[Union[str, Tuple[str, str]]]
    memory_instruction: MemoryGetInstruction

    def __init__(
        self, 
        identifiers: List[Union[str, Tuple[str, str]]],
        default: Optional[Dict[str, Any]]=None,
        memory_instruction: MemoryGetInstruction=MemoryGetInstruction.GET,
    ):
        """
        Args:
            identifiers (List[Union[str, Tuple[str, str]]]): Key/keys that will be used to
                access data in memory and for setting to register.

            default (Dict[str, Any]): A map of values to be returned for each provided identifier 
                if the identifier(s) are not found. If an identifier is not found and 
                no default value is provided for it, an exception will be raised. 
                Defaults to None.

            memory_instruction (MemoryGetInstruction, optional): Strategy for memory access.
                Defaults to MemoryGetInstruction.GET.
        """
        super().__init__()
        self.identifiers = identifiers
        self.default = default
        self.memory_instruction = memory_instruction

    
    def __call__(
        self, input_data: Transformable, evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        """
        Args:
            input_data (Transformable): Current data.

            evaluator (Optional[Evaluator], optional): Evaluator in context of which executed.
                If equals to None, default evaluator will be created. Defaults to None.

        Raises:
            InavalidMemoryInstruction: If provided instruction doesn't exist.

        Returns:
            Transformable: Result of execution.
        """
        if not evaluator:
            evaluator = self.set_up_default_evaluator()

        if self.memory_instruction == MemoryGetInstruction.GET:
            register = evaluator.get_memory(input_data, self.identifiers, self.default or {})
        elif self.memory_instruction == MemoryGetInstruction.POP:
            register = evaluator.get_memory(input_data, self.identifiers, self.default or {}, delete=True)
        else:
            raise InavalidMemoryInstruction()
        return register


class DeleteMemory(Component):
    """
    Delete data from memory
    """
    def __init__(
        self, identifiers: Optional[List[str]]=None,
    ):
        """
        Args:
            identifiers (Optional[List[str]], optional): Keys associated with data.
                If equals to None, flushes memory. Defaults to None.
        """
        self.identifiers = identifiers


    def __call__(
        self, input_data: Transformable, evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        """
        Args:
            input_data (Transformable): Current data.

            evaluator (Optional[Evaluator], optional): Evaluator in context of which executed.
                If equals to None, default evaluator will be created. Defaults to None.

        Returns:
            Transformable: Input data
        """
        if not evaluator:
            evaluator = self.set_up_default_evaluator()

        if not self.identifiers:
            evaluator.flush_memory()
        else:
            for i in self.identifiers:
                evaluator.delete_memory(i)
        return input_data


class MemoryManager:
    """
    Manage memory
    """
    memory: Memory

    def __init__(
        self, 
        path: Optional[str]=None, 
        initial_data: Optional[Dict[str, Any]]=None
    ) -> None:
        """
        Args:
            directory (Optional[str], optional): Path to directory. Defaults to None.
            
            initial_data (Optional[Dict[str, Any]], optional): Data for initialization 
                of memory. Defaults to None.
        """
        self.memory = Memory(path, initial_data)

        
    def get(
        self, 
        register: Transformable, 
        identifiers: List[Union[str, Tuple[str, str]]],
        default: Dict[str, Any],
        delete: bool=False
    ) -> Transformable:
        """
        Get data from memory

        Args:
            register (Transformable): Current data.

            identifiers (List[Union[str, Tuple[str, str]]]): Key/keys that will be used to
                access data in memory and for setting to register.

            default (Dict[str, Any]): A map of values to be returned for each provided identifier 
                if the identifier(s) are not found. If an identifier is not found and 
                no default value is provided for it, an exception will be raised. 
                Defaults to None.
            
            delete (bool, optional): If equals to True, deletes accessed memory identifiers. 
                Defaults to False.

        Returns:
            Transformable: Result of execution.
        """
        for identifier in identifiers:
            if isinstance(identifier, tuple):
                get_key = identifier[0]
                set_key = identifier[1]
            else:
                get_key = identifier
                set_key = identifier
            try:
                data = self.memory.retrieve_store(get_key)
            except:
                if not get_key in default:
                    raise KeyError(f"No specified identifier found: {get_key}")
                data = default[get_key]
            setattr(
                register,
                set_key,
                data
            )
            if delete:
                self.memory.delete_store(get_key)
        return register

        
    def set(
        self, 
        register: Transformable, 
        get_key: str,
        set_key: str,
    ) -> None:
        """
        Set data to memory

        Args:
            register (Transformable): Current data.

            get_key (str): Source of data.
            
            set_key (str): Destination in memory.
        """
        self.memory.add_store(
            set_key, getattr(register, get_key)
        )


    def delete(
        self, identifier: str
    ) -> None:
        """
        Delete specified identifier from memory

        Args:
            identifier (str): Identifier to delete.
        """
        self.memory.delete_store(identifier)
        

    def flush(self) -> None:
        """
        Clean memory
        """
        self.memory.flush()


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"