from __future__ import annotations
from typing import (
    Any, List, Dict, Type, Generic, Optional, TypeVar, cast
)
from abc import ABC,  abstractmethod

from core.executable_level_1.component import Component, Executor
from core.executable_level_1.schema import (
    InputType, 
    OutputType, 
    Transformable, 
    Input,
    Output
)
from core.executable_level_1.statements_types import (
    Statement
)

ValidationClass = TypeVar("ValidationClass", Input, Output)

class Executable(
    Generic[InputType, OutputType], 
    Component, 
    ABC
):
    default_key: str
    input_class: Type[InputType]
    output_class: Type[OutputType]

    def __init__(
        self, 
        input_class: Type[InputType]=Input,
        output_class: Type[OutputType]=Output, 
        default_key: str="output"
    ):
        self.input_class = input_class
        self.output_class = output_class
        self.default_key = default_key


    @abstractmethod
    def invoke(self, input_data: InputType) -> Dict[str, Any]:
        ...


    def validate(
        self, 
        data: Dict[str, Any],
        validation_class: Type[ValidationClass]
    ) -> ValidationClass:
        return validation_class(**data)


    def execute(
        self, 
        input_data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        try:
            validated_input = self.validate(
                input_data,
                self.input_class
            )
            result: Dict[str, Any] = self.invoke(validated_input)
            self.validate(
                result, self.output_class
            )
            return result
        except Exception as e:
            raise ValueError(f"Validation error: {e}")


    def execute_batch(
        self, 
        input_data: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        try:
            result: List[Dict[str, Any]] = []
            
            for i in input_data:
                validated_input = self.validate(i, self.input_class)
                tmp = self.invoke(validated_input)
                self.validate(tmp, self.output_class)
                result.append(tmp)
            return result
        except Exception as e:
            raise ValueError(f"Validation error: {e}")
    

    def __call__(
        self, 
        register: Transformable,
        get_key: Optional[str]=None,
        set_key: Optional[str]=None
    ) -> Transformable:
        input_data = getattr(register, get_key or "__dict__")
        if isinstance(input_data, Dict):
            result = self.execute(cast(Dict[str, Any], input_data))
            set_key = set_key or "__dict__"
        else:
            result = self.execute_batch(
                cast(List[Dict[str, Any]], input_data)
            )
            set_key = set_key or self.default_key
        setattr(
            register, 
            set_key,
            result
        )
        return register


    def use(
        self,
        get_key: Optional[str]=None,
        set_key: Optional[str]=None
    ) -> Executor:
        return Executor(
            component=self, 
            get_key=get_key, 
            set_key=set_key
        )


    def generate_statement(
        self
    ) -> Dict[str, Any]:
        return {
            "type": Statement.EXECUTE_STATEMENT,  
            Statement.EXECUTE_STATEMENT.value: self
        }