from typing import Any, Dict, Type
import logging

from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import Transformable, Input, Output
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


def test_executable():
    # use default overwrite behaviour
    input = {"f": 4}
    example = MyExecutable()

    logging.info(example.run(input).__repr__())

    # use get and set key
    logging.info(example.use(
        get_key="input",
        set_key="output"
    )(Transformable({"input": input})).__repr__())


def test_pipeline():
    example = MyExecutable()
    pipeline = (
        example
        | example
        | example.use(
            set_key="output"
        )
        | example.use(
            get_key="output",
            set_key="result"
        )
    )
    logging.info(pipeline.program)
    res = Evaluator(pipeline).run({"f": 1})
    logging.info(f"Pipeline res: {res}")