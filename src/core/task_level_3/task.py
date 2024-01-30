from abc import ABC, abstractmethod

from src.executable_level_1.executable import Executable
from src.executable_level_1.schema import InputType, OutputType
from src.model_level_2.model import Model

# Add abstraction, different tasks per one model
# Maybe push it inside model
class Task(Executable[InputType, OutputType], ABC):
    model: Model[InputType, OutputType]
    task: str

    def __init__(self, model: Model[InputType, OutputType], taskName: str) -> None:
        self.taks = taskName
        self.model = model


    @abstractmethod
    def preprocess(self, input_data: InputType) -> InputType:
        # add prompt
        pass


    def invoke(self, input_data: InputType) -> OutputType:
        return self.model.invoke(input_data)


    @abstractmethod
    def postprocess(self, output_data: OutputType) -> OutputType:
        pass


    @abstractmethod
    def process(self, input_data: InputType):
        self.postprocess(
            self.invoke(
                self.preprocess(input_data)
            )
        )