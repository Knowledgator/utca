from typing import Any, Generic, Type, Dict

from abc import ABC,  abstractmethod

from schema import   InputType,  OutputType


class Validator(Generic[InputType]):
    def __init__(self, input_validation: Type[InputType]) -> None:
        self.input_validation = input_validation

    def validate(self, toValidate: Dict[str, Any]) -> InputType:
        return self.input_validation(**toValidate)



# ! modularity, diff input, particular output
# log
# state saver
# stopable
# exseptions
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

    def execute(self, input_data: Dict[str, Any], isdict) -> Dict[str, Any]:
        # switch
        try:
            validated_input = self.validate_input(input_data)
            result = self.invoke(validated_input)
            self.validate_output(result)
            return result
        except Exception as e:
            raise ValueError(f"Validation error: {e}")
    def getValidator(self) -> Validator[InputType]:
        return Validator(self.input_class)


