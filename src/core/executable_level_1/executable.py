from typing import Any, Generic, Type, Dict, Union, overload

from abc import ABC,  abstractmethod
from core.executable_level_1.transformable import Transformable, Validator

from schema import   InputType,  OutputType





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


    @overload
    def execute(
        self, 
        input_data: Union[Dict[str, Any], InputType, Transformable], 
        return_type: Type[Dict[str, Any]]
    ) -> Dict[str, Any]:
        ...


    @overload
    def execute(
        self, 
        input_data: Union[Dict[str, Any], InputType, Transformable], 
        return_type: Type[OutputType]
    ) -> OutputType:
        ...


    @overload
    def execute(
        self, 
        input_data: Union[Dict[str, Any], InputType, Transformable], 
        return_type: Type[Transformable]
    ) -> Transformable:
        ...


    def execute(
        self, 
        input_data: Union[Dict[str, Any], InputType, Transformable], 
        return_type: Type[Union[Dict[str, Any], OutputType, Transformable]]
    ) -> Union[Dict[str, Any], OutputType, Transformable]:
        try:
            if isinstance(input_data, Transformable):
                extracted_dict = input_data.extract()
                validated_input = self.validate_input(extracted_dict)
            elif isinstance(input_data, Dict):
                validated_input = self.validate_input(input_data)
            else:
                validated_input = input_data
                
            result: Dict[str, Any] = self.invoke(validated_input)
            output = self.validate_output(result)

            if return_type is Transformable:
                return output.get_transform()
            elif return_type is Dict:
                return result
            else:
                return output
        except Exception as e:
            raise ValueError(f"Validation error: {e}")
    def getValidator(self) -> Validator[InputType]:
        return Validator(self.input_class)


