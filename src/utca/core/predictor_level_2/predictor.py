from typing import Any
from abc import abstractmethod

from utca.core.executable_level_1.executable import Executable
from utca.core.executable_level_1.schema import Input, Output

class Predictor(Executable[Input, Output]):
    """
    Base predictor class
    """
    @property
    @abstractmethod
    def config(self) -> Any:
        """
        Predictor configuration
        """
        ...