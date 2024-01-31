from typing import Dict, Any, Type
from abc import ABC, abstractmethod

from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import InputType, OutputType
from core.model_level_2.model import Model, ModelConfigs
from core.model_level_2.schema import PromptTemplate


# class TaskConfig

# Add abstraction, different tasks per one model
# Maybe push it inside model
class Task(Executable[InputType, OutputType], ABC):
    model_type: Type[Model[InputType]]
    template: PromptTemplate

    def __init__(self, taskName: str, cfg: ModelConfigs) -> None:
        self.taks = taskName
        self.model = self.model_type(cfg)


    @abstractmethod
    def preprocess(self, input_data: InputType) -> InputType:
        # add prompt
        pass
    
    
    @abstractmethod
    def postprocess(self, output_data: Dict[str, Any]) -> Dict[str, Any]:
        pass


    def invoke(self, input_data: InputType) -> Dict[str, Any]:
        return self.postprocess(self.model.invoke(self.preprocess(input_data)))
        