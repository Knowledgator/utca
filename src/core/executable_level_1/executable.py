from __future__ import annotations
from typing import (
    Any, Dict, Type, Generic, Optional, TypeVar, TYPE_CHECKING
)
from abc import ABC, abstractmethod

from pydantic import ValidationError

from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.component import Component
from core.executable_level_1.schema import (
    Input, 
    Output,
    IOModel,
    Transformable, 
)
from core.exceptions import ExecutableError
if TYPE_CHECKING:
    from core.executable_level_1.executor import ExecutableExecutor

ValidationClass = TypeVar("ValidationClass", bound=IOModel)

class Executable(
    Generic[Input, Output], 
    Component, 
    ABC
):
    input_class: Type[Input]
    output_class: Type[Output]

    def __init__(
        self, 
        input_class: Type[Input],
        output_class: Type[Output], 
        name: Optional[str]=None,
    ):
        super().__init__(name)
        self.input_class = input_class
        self.output_class = output_class


    @abstractmethod
    def invoke(self, input_data: Input, evaluator: Evaluator) -> Dict[str, Any]:
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
        
    
    def validate_input(self, data: Dict[str, Any]) -> Input:
        return self.validate(
            data, self.input_class
        )
        
    
    def validate_output(self, data: Dict[str, Any]) -> Output:
        return self.validate(
            data, self.output_class
        )


    def execute(
        self, 
        input_data: Dict[str, Any],
        evaluator: Evaluator
    ) -> Dict[str, Any]:
        try:
            return self.validate_output(
                self.invoke(
                    self.validate_input(input_data),
                    evaluator
                )
            ).extract()
        except Exception as e:
            raise ExecutableError(self.name, e)
    
    
    def __call__(
        self, 
        input_data: Transformable,
        evaluator: Optional[Evaluator]=None
    ) -> Transformable:
        if not evaluator:
            evaluator = self.set_up_default_evaluator()
        result = self.execute(input_data.__dict__, evaluator)
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