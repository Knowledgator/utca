from core.executable_level_1.__test__.utils import MyExecutable

def test_executable():
    # use default overwrite behaviour
    inputs = {"f": 4}
    example = MyExecutable()

    res = example.run(inputs)
    assert res == {"f": 5}


def test_executable_executor():
    inputs = {"f": 4}
    example = MyExecutable()

    # use get and set key
    res = example.use(
        get_key="input",
        set_key="output"
    ).run({"input": inputs})

    assert res == {
        "input": {"f": 4},
        "output": {"f": 5}
    }