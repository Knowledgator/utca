from typing import Any, Generic, Type, Dict, Union

from abc import ABC,  abstractmethod
from core.executable_level_1.transformable import Transformable

from schema import   InputType,  OutputType


class Validator(Generic[InputType]):
    def __init__(self, input_validation: Type[InputType]) -> None:
        self.input_validation = input_validation

    def validate(self, toValidate: Dict[str, Any]) -> InputType:
        return self.input_validation(**toValidate)


# + and | code
# protocol with transformable

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

    def execute(self, input_data: Union[Dict[str, Any], InputType, Transformable], return_dict: bool = False) -> Union[Dict[str, Any], OutputType, Transformable]:
        try:
            if isinstance(input_data, Transformable):
                extracted_dict = input_data.extract()
                validated_input = self.validate_input(extracted_dict)
            elif isinstance(input_data, Dict):
                validated_input = self.validate_input(input_data)
            else:
                validated_input = input_data
            result = self.invoke(validated_input)
            output = self.validate_output(result)

            if not return_dict:
                return output
            else:
                return result
        except Exception as e:
            raise ValueError(f"Validation error: {e}")
    def getValidator(self) -> Validator[InputType]:
        return Validator(self.input_class)


