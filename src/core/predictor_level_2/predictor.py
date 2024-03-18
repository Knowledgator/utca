from typing import Any
from abc import abstractmethod

from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import InputType, OutputType

class Predictor(Executable[InputType, OutputType]):
    @property
    @abstractmethod
    def config(self) -> Any:
        ...