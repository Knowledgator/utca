from typing import TypeVar, Generic
from abc import ABC, abstractmethod


InputType = TypeVar('InputType') # can be send more general
OutputType = TypeVar('OutputType')


class IOValidator(Generic[InputType, OutputType]):
    def __init__(self, input: InputType, output: OutputType) -> None:
        self.input = input
        self.output = output
    @abstractmethod
    def isValidInput(self, input_data: InputType) -> bool:
        pass
    @abstractmethod
    def isValidOutput(self, output_data: OutputType) -> bool:
        pass

    def parse(self, content: str):
        # Implement parsing logic
        pass
    
    def loadSchema(self, path: str ="."):
        with open(path, "r") as file:
            content = file.read()
            self.parse(content)



class Input(ABC):
    # def __init__(self, value: Optional[Dict[Any, Any]] = None) -> None: 
    #     self.value = value if value is not None else {}
    # value: Dict[Any, Any]
    pass

class Output(ABC):
    # Define necessary methods or properties
    pass

# потом дженерик можно заменить на что то subtyped
class Executable(Generic[InputType, OutputType], ABC):

    def __init__(self, validator: IOValidator[InputType, OutputType]):
        self.validator = validator

    def execute(self, input_data: InputType) -> OutputType:
        if not self.validator.isValidInput(input_data):
            raise ValueError("Invalid input")
        result = self.invoke(input_data)
        if not self.validator.isValidOutput(result):
            raise ValueError("Invalid output")
        return result

    @abstractmethod
    def invoke(self, input_data: InputType) -> OutputType:
        pass

