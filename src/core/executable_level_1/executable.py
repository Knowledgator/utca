from typing import Any, Generic, Type, Dict

from abc import ABC,  abstractmethod

from schema import  InputType,  OutputType

INPUT_SCHEMA_PATH = "/io/input_schema.json"
OUTPUT_SCHEMA_PATH = "/io/output_schema.json"

# InputType = TypeVar('InputType') # can be send more general
# OutputType = TypeVar('OutputType')


class IOValidator(ABC):
    def __init__(self) -> None:
        # work with input schema
        pass

    @abstractmethod
    def isValidInput(self) -> bool:
        pass
    @abstractmethod
    def isValidOutput(self) -> bool:
        pass


# log
# state saver
# stopable
class Executable(Generic[InputType, OutputType], ABC):
    input_class: Type[InputType]
    output_class: Type[OutputType]
    def __init__(self):
        pass
        
    @abstractmethod
    def invoke(self, input_data: InputType) -> Dict[str, Any]:
        pass


    def validate_input(self, input_data: Dict[str, Any]) -> InputType:
        return self.input_class(**input_data)


    def validate_output(self, output_data: Dict[str, Any]) -> OutputType:
        return self.output_class(**output_data)


    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        try:
            validated_input = self.validate_input(input_data)
            result = self.invoke(validated_input)
            self.validate_output(result)
            return result
        except Exception as e:
            raise ValueError(f"Validation error: {e}")



