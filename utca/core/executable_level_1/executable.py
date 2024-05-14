from __future__ import annotations
from typing import (
    Any, Dict, Type, Generic, Optional, TypeVar, TYPE_CHECKING
)
from abc import abstractmethod

from pydantic import ValidationError

from utca.core.executable_level_1.interpreter import Evaluator
from utca.core.executable_level_1.component import Component
from utca.core.executable_level_1.schema import (
    Input, 
    Output,
    IOModel,
    Transformable, 
    ReplacingScope,
)
from utca.core.exceptions import ExecutableError, IvalidInputData
if TYPE_CHECKING:
    from utca.core.executable_level_1.executor import ExecutableExecutor

ValidationClass = TypeVar("ValidationClass", bound=IOModel)
"""
Type variable for validation classes
"""

class Executable(
    Generic[Input, Output], 
    Component, 
):
    """
    Base class for executables
    """
    input_class: Type[Input]
    output_class: Type[Output]

    def __init__(
        self, 
        input_class: Type[Input],
        output_class: Type[Output], 
        name: Optional[str]=None,
        replace: ReplacingScope=ReplacingScope.INPLACE,
    ):
        """
        Args:
            input_class (Type[Input]): Class for input validation.

            output_class (Type[Output]): Class for output validation.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
            
            replace (ReplacingScope, optional): Replacing strategy. Defaults to ReplacingScope.INPLACE.
        """
        super().__init__(name)
        self.input_class = input_class
        self.output_class = output_class
        self.replace = replace


    @abstractmethod
    def invoke(self, input_data: Input, evaluator: Evaluator) -> Dict[str, Any]:
        """
        Main logic

        Args:
            input_data (Input): Validated input.

            evaluator (Evaluator): Evaluator in context of which executed.

        Returns:
            Dict[str, Any]: Result of execution.
        """
        ...


    def validate(
        self, 
        data: Dict[str, Any],
        validation_class: Type[ValidationClass]
    ) -> ValidationClass:
        """
        Validation of input/output

        Args:
            data (Dict[str, Any]): Input/output data.

            validation_class (Type[ValidationClass]): Class used for validation.

        Raises:
            IvalidInputDataValue: If data is invalid.

        Returns:
            ValidationClass: Validated data.
        """
        try:
            return validation_class(**data)
        except ValidationError as e:
            raise IvalidInputData(
                f"Input validation error: {e.json()}: "
                f"Expected schema class: {validation_class!r}: "
                f"Expected schema: {validation_class.model_json_schema()}"
            )
        
    
    def validate_input(self, data: Dict[str, Any]) -> Input:
        """
        Validation of input

        Args:
            data (Dict[str, Any]): Input data.

        Returns:
            Input: Validated input.
        """
        return self.validate(
            data, self.input_class
        )
        
    
    def validate_output(self, data: Dict[str, Any]) -> Output:
        """
        Validation of output

        Args:
            data (Dict[str, Any]): Output data.

        Returns:
            Input: Validated output.
        """
        return self.validate(
            data, self.output_class
        )


    def execute(
        self, 
        input_data: Dict[str, Any],
        evaluator: Evaluator
    ) -> Dict[str, Any]:
        """
        Validate input, invoke and validate output

        Args:
            input_data (Dict[str, Any]): Data for processing.

            evaluator (Evaluator): Evaluator in context of which executed.

        Raises:
            ExecutableError: If any error occur.

        Returns:
            Dict[str, Any]: Result of execution.
        """
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
        """
        Args:
            input_data (Transformable): Data that is used in executable.

            evaluator (Optional[Evaluator], optional): Evaluator in context of which executable executed.
                If equals to None, default evaluator will be created. Defaults to None.

        Returns:
            Transformable: Result of execution.
        """
        if not evaluator:
            evaluator = self.set_up_default_evaluator()
        result = self.execute(input_data.__dict__, evaluator)
        if self.replace in (ReplacingScope.GLOBAL, ReplacingScope.LOCAL):
            return Transformable(result)
        input_data.update(result)
        return input_data


    def use(
        self,
        get_key: Optional[str]=None,
        set_key: Optional[str]=None,
        default_key: str="output",
        replace: Optional[ReplacingScope]=None,
    ) -> ExecutableExecutor:
        """
        Creates ExecutableExecutor which manages context

        Args:
            get_key (Optional[str], optional): Which key value of input_data will be used. 
                If value equal to None, root dict will be used. Defaults to None.

            set_key (Optional[str], optional): Which key will be used to set result value. 
                If set_key value equal to None:
                    - if result of type Dict[str, Any], update root dict;
                    - else, set result to default_key.
                Defaults to None.

            default_key (str, optional): Default key used for results that is not of type Dict.
                Defaults to "output".

            replace (Optional[ReplacingScope], optional): Replacing strategy for executor.
                If equals to None, this executable strategy will be used. Defaults to None.

        Returns:
            ExecutableExecutor: Wrapper of Executable
        """
        from utca.core.executable_level_1.executor import ExecutableExecutor
        return ExecutableExecutor(
            component=self, 
            get_key=get_key, 
            set_key=set_key,
            default_key=default_key,
            replace=replace or self.replace,
        )