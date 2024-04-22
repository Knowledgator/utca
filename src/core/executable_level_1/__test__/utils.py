from typing import Any, Dict, Type

from core.executable_level_1.schema import IOModel
from core.executable_level_1.executable import Executable
from core.executable_level_1.interpreter import Evaluator

class MyIO(IOModel):
    f: int


class MyExecutable(Executable[MyIO, MyIO]):
    def __init__(
        self, 
        input_class: Type[MyIO]=MyIO, 
        output_class: Type[MyIO]=MyIO, 
    ):
        super().__init__(input_class, output_class)


    def invoke(self, input_data: MyIO, evaluator: Evaluator) -> Dict[str, Any]:
        # Implementation of the processing logic
        return {"f": input_data.f + 1}