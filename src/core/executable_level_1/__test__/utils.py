from typing import Any, Dict, Type

from core.executable_level_1.schema import Input, Output
from core.executable_level_1.executable import Executable
from core.executable_level_1.interpreter import Evaluator

class MyInput(Input):
    f: int


class MyOutput(Output):
    f: int


class MyExecutable(Executable[MyInput, MyOutput]):
    input_class = MyInput
    output_class = MyOutput

    def __init__(
        self, 
        input_class: Type[MyInput]=MyInput, 
        output_class: Type[MyOutput]=MyOutput, 
    ):
        super().__init__(input_class, output_class)


    def invoke(self, input_data: MyInput, evaluator: Evaluator) -> Dict[str, Any]:
        # Implementation of the processing logic
        return {"f": input_data.f + 1}