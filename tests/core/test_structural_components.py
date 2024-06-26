from typing import Any, Dict, List
import copy
import logging
import io


from .utils import MyExecutable
from utca.core import (
    Evaluator,
    While, 
    Transformable, 
    Condition, 
    ExecuteFunction,
    ForEach,
    Branch,
    Switch,
    Filter,
    Log,
    BREAK,
)

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
    assert len(pipeline.program) == 4
    res = pipeline.run({"f": 1})
    assert res["result"]["f"] == 5


def test_loop_function_condition():
    def function_condition(input_data: Transformable, evaluator: Evaluator) -> bool:
        data = input_data.extract()
        return data["f"] < 5
    example = MyExecutable()
    
    loop = While(
        condition=function_condition,
        schema=example,
    )

    res = loop.run({"f": 0})
    assert res["f"] == 5


def test_loop_obj_condition():
    def f(x: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "f": x["f"] % 10
        }
    condition_schema = ExecuteFunction(f)
    condition = Condition(
        validator=lambda x, e: x.__dict__["f"] != 0, # type: ignore
        schema=condition_schema,
    )

    example = MyExecutable()
    
    loop = While(
        condition=condition,
        schema=example,
    )

    res = loop.run({"f": 1})
    assert res["f"] == 10


def test_loop_iterations():
    example = MyExecutable()
    
    loop = While(
        schema=example,
        max_iterations=10
    )

    res = loop.run({"f": 0})
    assert res["f"] == 10


def test_loop_exit():
    example = MyExecutable()
    
    loop = While(
        schema=BREAK | example,
        max_iterations=10
    )

    res = loop.run({"f": 0})
    assert res["f"] == 0


def test_for_each():
    def check(
        inputs: List[Dict[str, int]], 
        outputs: List[Dict[str, int]]
    ) -> None:
        for i, o in zip(inputs, outputs):
            assert i["f"] + 1 == o["f"]

    inputs = {
        "fs": [
            {"f": i} for i in range(10)
        ]
    }
    example = MyExecutable()
    
    res = ForEach(
        schema=example,
        get_key="fs",
    ).run(copy.deepcopy(inputs))
    check(inputs["fs"], res["fs"])

    res = ForEach(
        schema=example,
        get_key="fs",
        set_key="results"
    ).run(res)
    check(res["fs"], res["results"])


def test_switch_default_branch():
    example = MyExecutable()
    res = Switch(
        Branch(
            example
        ),
        Branch( # should not be triggered. Branch above will be triggered and exit.
            example
        ),
        name="MySwitch"
    ).run({
        "f": 0
    })
    assert res["f"] == 1 # executed once


def test_switch_default_branch_no_exit():
    example = MyExecutable()
    res = Switch(
        Branch(
            example,
            exit_branch=False,
        ),
        Branch( # should be triggered. Branch above will be triggered and not exited.
            example
        ),
        name="MySwitch"
    ).run({
        "f": 0
    })
    assert res["f"] == 2 # executed twice


def test_switch_order():
    example = MyExecutable()
    res = Switch(
        Branch(
            example
        ),
        Branch(
            example,
            exit_branch=False,
        ),
        name="MySwitch"
    ).run({
        "f": 0
    })
    assert res["f"] == 1 # executed once


def test_switch_conditions():
    example = MyExecutable()
    def function_condition(input_data: Transformable, evaluator: Evaluator) -> bool:
        data = input_data.extract()
        return data["f"] > 3

    def f(x: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "f": x["f"] % 2
        }
    condition_schema = ExecuteFunction(f)
    obj_condition = Condition(
        validator=lambda x, e: x.__dict__["f"] == 0, # type: ignore
        schema=condition_schema,
    )

    s = Evaluator(Switch(
            Branch( # if f % 2 == 0
                example | example | example, # +3
                condition=obj_condition,
            ),
            Branch( # elif f > 3
                example | example, # +2
                condition=function_condition,
            ),
            Branch( # else
                example, # +1 
            ),
            name="MySwitch"
        ),
        logging_level=logging.WARNING
    )

    for i in range(10000):
        res = s.run({"f": i})["f"]
        if i % 2 == 0:
            assert i + 3 == res
        elif i > 3:
            assert i + 2 == res
        else:
            assert i + 1 == res


def test_filter():
    def function_condition(input_data: Transformable, evaluator: Evaluator) -> bool:
        data = input_data.extract()
        return data["f"] > 25

    def f(x: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "f": x["f"] % 5
        }
    condition_schema = ExecuteFunction(f)
    obj_condition = Condition(
        validator=lambda x, e: x.__dict__["f"] == 0, # type: ignore
        schema=condition_schema,
    )

    filter1 = Filter(
        condition=function_condition,
        get_key="fs",
    )
    filter2 = Filter(
        condition=obj_condition,
        get_key="fs",
    )

    res = filter1.run({
        "fs": [{"f": i} for i in range(100)]
    })
    assert res["fs"][0]["f"] == 26
    assert res["fs"][-1]["f"] == 99

    res = filter2.run(res)
    for i in res["fs"]:
        assert i["f"] % 5 == 0


def test_log_with_logger():
    stream = io.StringIO()
    logging_handler = logging.StreamHandler(stream)
    logger = logging.getLogger("TEST")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging_handler)

    log = Log(logging.DEBUG, logger, message="OK", include_input_data=False)
    log.run({})

    stream.flush()
    assert "OK" in stream.getvalue()
    stream.truncate(0)
    assert "" == stream.getvalue()

    logger.setLevel(logging.ERROR)

    log.run({})
    stream.flush()
    assert "" == stream.getvalue()
    stream.close()


def test_log_inside_evaluator():
    stream = io.StringIO()
    e = Evaluator(
        (
            Log(logging.INFO, message="OK")
            | Log(logging.DEBUG, message="ERROR")
            | Log(logging.ERROR, message="NICE")
        ), 
        name="TestEvaluator",
        logging_level=logging.INFO,
        logging_handler=logging.StreamHandler(stream)
    )
    e.run({})

    stream.flush()
    res = stream.getvalue()
    assert "OK" in res
    assert "ERROR" not in res
    assert "NICE" in res