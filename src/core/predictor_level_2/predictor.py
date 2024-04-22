from typing import Any
from abc import abstractmethod

from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import Input, Output

class Predictor(Executable[Input, Output]):
    @property
    @abstractmethod
    def config(self) -> Any:
        ...