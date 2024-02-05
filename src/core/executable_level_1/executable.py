from typing import Any, Generic, Type, Dict, Union, overload, Optional, cast

from abc import ABC,  abstractmethod

from core.executable_level_1.schema import InputType, OutputType, ConfigType, Transformable, Validator


# + and | code
# protocol with transformable

class Executable(Generic[ConfigType, InputType, OutputType], ABC):
    input_class: Type[InputType]
    output_class: Type[OutputType]

    def __init__(self, cfg: ConfigType) -> None:
        self.cfg = cfg


    @abstractmethod
    def invoke(self, input_data: InputType) -> Dict[str, Any]:
        ...


    @abstractmethod
    def invoke_batch(self, input_data: list[InputType]) -> list[Dict[str, Any]]:
        ...


    def validate_input(
        self, input_data: Union[Dict[str, Any], InputType, Transformable]
    ) -> InputType:
        if isinstance(input_data, Transformable):
            extracted_dict = input_data.extract()
            return self.input_class(**extracted_dict)
        elif isinstance(input_data, Dict):
            return self.validate_input(**input_data)
        else:
            return input_data


    def validate_output(self, output_data: Dict[str, Any]) -> OutputType:
        return self.output_class(**output_data)


    def prepare_output(
        self, 
        output_data: Dict[str, Any], 
        return_type: Optional[Type[Union[Dict[str, Any], Transformable]]]=None
    ) -> Union[Dict[str, Any], OutputType, Transformable]:
        output = self.validate_output(output_data)
        if return_type is Transformable:
            return output.get_transform()
        elif return_type is Dict[str, Any]:
            return output_data
        else:
            return output


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
        return_type: None=None
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
        return_type: Optional[Type[Union[Dict[str, Any], Transformable]]]=None
    ) -> Union[Dict[str, Any], OutputType, Transformable]:
        try:
            validated_input = self.validate_input(input_data)
            result: Dict[str, Any] = self.invoke(validated_input)
            return self.prepare_output(result, return_type)
        except Exception as e:
            raise ValueError(f"Validation error: {e}")
        
    
    @overload
    def execute_batch(
        self, 
        input_data: list[Union[Dict[str, Any], InputType, Transformable]], 
        return_type: Type[Dict[str, Any]]
    ) -> list[Dict[str, Any]]:
        ...


    @overload
    def execute_batch(
        self, 
        input_data: list[Union[Dict[str, Any], InputType, Transformable]], 
        return_type: None=None
    ) -> list[OutputType]:
        ...


    @overload
    def execute_batch(
        self, 
        input_data: list[Union[Dict[str, Any], InputType, Transformable]], 
        return_type: Type[Transformable]
    ) -> list[Transformable]:
        ...


    def execute_batch(
        self, 
        input_data: list[Union[Dict[str, Any], InputType, Transformable]], 
        return_type: Optional[Type[Union[Dict[str, Any], Transformable]]]=None
    ) -> Union[list[Dict[str, Any]], list[OutputType], list[Transformable]]:
        try:
            validated_input = [
                self.validate_input(i) for i in input_data
            ]
            result: list[Dict[str, Any]] = self.invoke_batch(validated_input)
            return cast(
                Union[list[Dict[str, Any]], list[OutputType], list[Transformable]],
                [
                    self.prepare_output(r, return_type) for r in result
                ]
            )
        except Exception as e:
            raise ValueError(f"Validation error: {e}")


    def getValidator(self) -> Validator[InputType]:
        return Validator(self.input_class)


