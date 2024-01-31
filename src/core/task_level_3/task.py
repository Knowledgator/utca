from typing import Dict, Any
from abc import ABC, abstractmethod

from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import InputType, OutputType
from core.model_level_2.model import Model

# Add abstraction, different tasks per one model
# Maybe push it inside model
class Task(Executable[InputType, OutputType], ABC):
    def __init__(self, model: Model[InputType], taskName: str) -> None:
        self.taks = taskName
        self.model = model
    prompt: str
    prompt_len: int

    @abstractmethod
    def preprocess(self, input_data: InputType) -> InputType:
        # add prompt
        pass
    
    
    @abstractmethod
    def postprocess(self, output_data: Dict[str, Any]) -> Dict[str, Any]:
        pass


    @abstractmethod
    def invoke(self, input_data: InputType) -> Dict[str, Any]:
        self.postprocess(self.model.invoke(self.preprocess(input_data)))
        