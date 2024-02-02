# Example subclass implementation
from typing import Any, Dict
from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import Input, Output


class MyInput(Input):
    # Input class implementation goes here
    f: str
    pass

class MyOutput(Output):
    # Output class implementation goes here
    pass

class MyExecutable(Executable[MyInput, MyOutput]):
    input_class = MyInput
    output_class = MyOutput

    def invoke(self, input_data: MyInput) -> Dict[str, Any]:
        # Implementation of the processing logic
        return {"f": 5}
    
input = {"f": 4}
example = MyExecutable()

print(example.execute(input))