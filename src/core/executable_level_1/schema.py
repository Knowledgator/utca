from __future__ import annotations
from abc import ABC
from typing import (
    Optional, TypeVar, Any, Dict
)
from enum import Enum

from pydantic import BaseModel

class IOModel(BaseModel, ABC):
    def generate_transformable(self):
        """
        Create Transformable from this class

        Returns:
            Transformable: Transformable representation of the class
        """
        return Transformable(self.extract())
    

    def extract(self) -> Dict[str, Any]:
        """
        Unpack data from this class and return Dict[str, Any]

        Returns:
            Dict[str, Any]: Data packed in the class
        """
        return self.model_dump()


# Task №1 - can validate is it right based on input and output class !!!
class Transformable:
    """
    Data manager class
    """
    def __init__(self, state: Optional[Dict[str, Any]]=None) -> None:
        """
        Args:
            state (Optional[Dict[str, Any]], optional): Data to wrapp. 
                Defaults to None.
        """
        self.__dict__ = state or {}
    

    def extract(self) -> Dict[str, Any]:
        """
        Unpack data from this class and return Dict[str, Any]

        Returns:
            Dict[str, Any]: Data packed in the class
        """
        return self.__dict__
    

    def update(self, data: Dict[str, Any]) -> None:
        """
        Add data to class

        Args:
            data (Dict[str, Any]): Data to add
        """
        self.__dict__.update(data)

    
    def flush(self) -> None:
        """
        Remove all data
        """
        self.__dict__ = {}


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"


class Config(BaseModel, ABC):
    """
    Base config class
    """
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"


Input = TypeVar('Input', bound=IOModel)
Output = TypeVar('Output', bound=IOModel)


class ReplacingScope(Enum):
    INPLACE = 0
    """
    Rewrite only keys in specified scope
    """
    LOCAL = 1
    """
    Rewrite only specified scope
    """
    GLOBAL = 2
    """
    Rewrite data completely
    """
    