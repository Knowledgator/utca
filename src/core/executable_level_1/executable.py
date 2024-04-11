from __future__ import annotations
from typing import (
    Any, List, Dict, Type, Generic, Optional, 
    TypeVar, TYPE_CHECKING, cast
)
from abc import ABC,  abstractmethod

from pydantic import ValidationError

from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.component import Component
from core.executable_level_1.schema import (
    InputType, 
    OutputType, 
    Transformable, 
    Input,
    Output
)
if TYPE_CHECKING:
    from core.executable_level_1.executor import ExecutableExecutor

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


    def ensure_dict(self, input_data: Any) -> Dict[str, Any]:
        return (
            {
                self.default_key: input_data
            } 
            if not isinstance(input_data, Dict) 
            else cast(Dict[str, Any], input_data)
        )


    @abstractmethod
    def invoke(self, input_data: InputType, evaluator: Evaluator) -> Dict[str, Any]:
        ...


    def validate(
        self, 
        data: Dict[str, Any],
        validation_class: Type[ValidationClass]
    ) -> ValidationClass:
        try:
            return validation_class(**data)
        except ValidationError as e:
            raise ValueError(
                f"Input validation error: {e.json()}: "
                f"Expected schema class: {validation_class!r}: "
                f"Expected schema: {validation_class.model_json_schema()}"
            )
        

    def execute(
        self, 
        input_data: Dict[str, Any],
        evaluator: Evaluator
    ) -> Dict[str, Any]:
        validated_input = self.validate(
            input_data,
            self.input_class
        )
        
        try:
            result: Dict[str, Any] = self.invoke(validated_input, evaluator)
        except Exception as e:
            raise Exception(f"Error durring execution: {self.__class__}: {e}")
        
        return self.validate(
            result, self.output_class
        ).model_dump()


    def execute_batch(
        self, 
        input_data: List[Dict[str, Any]],
        evaluator: Evaluator
    ) -> List[Dict[str, Any]]:
        result: List[Dict[str, Any]] = []

        for i in input_data:
            validated_input = self.validate(i, self.input_class)
            try:
                tmp = self.invoke(validated_input, evaluator)
            except Exception as e:
                raise Exception(
                    f"Error durring execution: {self.__class__}: {e}"
                )
            self.validate(tmp, self.output_class)
            result.append({
                **i,
                **tmp,
            })
        return result
    
    
    def __call__(
        self, 
        input_data: Transformable,
        evaluator: Evaluator
    ) -> Transformable:
        data = input_data.__dict__
        result = self.execute(data, evaluator)
        input_data.update(result)
        return input_data


    def use(
        self,
        get_key: Optional[str]=None,
        set_key: Optional[str]=None
    ) -> ExecutableExecutor:
        from core.executable_level_1.executor import ExecutableExecutor
        return ExecutableExecutor(
            component=self, 
            get_key=get_key, 
            set_key=set_key
        )