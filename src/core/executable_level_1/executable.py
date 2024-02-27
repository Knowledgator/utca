from __future__ import annotations
from typing import (
    Any, List, Type, Dict, Union, cast, Generic, Optional
)
from abc import ABC,  abstractmethod

from core.executable_level_1.component import Component
from core.executable_level_1.schema import (
    ConfigType, 
    InputType, 
    OutputType, 
    Transformable, 
    Validator,
    Input,
    Output
)
from core.executable_level_1.statements_types import (
    Statement
)

# + and | code
# protocol with transformable

class Executable(Generic[ConfigType, InputType, OutputType], Component, ABC):
    input_class: Type[InputType]
    output_class: Type[OutputType]

    def __init__(
        self, 
        cfg: Optional[ConfigType]=None,
        input_class: Type[InputType]=Input,
        output_class: Type[OutputType]=Output, 
    ):
        self.input_class = input_class
        self.output_class = output_class
        super().__init__(cfg)


    @abstractmethod
    def invoke(self, input_data: InputType) -> Dict[str, Any]:
        ...


    @abstractmethod
    def invoke_batch(self, input_data: list[InputType]) -> list[Dict[str, Any]]:
        ...


    def validate_input(
        self, input_data: Transformable
    ) -> Union[InputType, List[InputType]]:
        if not input_data.is_batch:
            return self.input_class(**cast(
                Dict[str, Any], input_data.extract()
            ))
        
        data = input_data.extract()
        return [
            self.input_class(
                **cast(Dict[str, Any], i)
            ) for i in data
        ]


    def validate_output(self, output_data: Dict[str, Any]) -> OutputType:
        return self.output_class(**output_data)


    def prepare_output(
        self, 
        output_data: Dict[str, Any], 
    ) -> Transformable:
        output = self.validate_output(output_data)
        return output.get_transform()


    def execute(
        self, 
        input_data: Transformable, 
    ) -> Transformable:
        try:
            validated_input = cast(InputType, self.validate_input(input_data))
            result: Dict[str, Any] = self.invoke(validated_input)
            return self.prepare_output(result)
        except Exception as e:
            raise ValueError(f"Validation error: {e}")


    def execute_batch(
        self, input_data: Transformable 
    ) -> Transformable:
        try:
            validated_input = cast(List[InputType], self.validate_input(input_data))
            result: list[Dict[str, Any]] = self.invoke_batch(validated_input)
            return Transformable(result)
        except Exception as e:
            raise ValueError(f"Validation error: {e}")


    def getValidator(self) -> Validator[InputType]:
        return Validator(self.input_class)
    

    def generate_statement(
        self
    ) -> Dict[str, Any]:
        return {"type": Statement.EXECUTE_STATEMENT,  Statement.EXECUTE_STATEMENT.value: self}


