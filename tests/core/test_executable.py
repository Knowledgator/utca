from .utils import MyExecutable

from utca.core import ReplacingScope

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


def test_executable_replacing_scopes_and_default_key():
    e = MyExecutable()

    # test LOCAL
    assert e.use(replace=ReplacingScope.LOCAL).run({"f": 0}) == {"f": 1}
    assert e.use("a", replace=ReplacingScope.LOCAL).run({"a": {"f": 0}, "b": 1}) == {
        "f": 1
    }
    assert e.use("a", replace=ReplacingScope.LOCAL).run({"a": [{"f": 0}]}) == {
        "a": [{"f": 0}],
        "output": [{"f": 1}]
    }
    assert e.use("a", "a", replace=ReplacingScope.LOCAL).run({"a": {"f": 0, "b": 1}}) == {
        "a": {"f": 1}
    }
    assert e.use("a", "a", replace=ReplacingScope.LOCAL).run({"a": [{"f": 0}], "b": 1}) == {
        "a": [{"f": 1}],
        "b": 1
    }

    # test GLOBAL
    assert e.use(replace=ReplacingScope.GLOBAL).run({"f": 0}) == {"f": 1}
    assert e.use("a", replace=ReplacingScope.GLOBAL).run({"a": {"f": 0}, "b": 1}) == {
        "f": 1
    }
    assert e.use("a", replace=ReplacingScope.GLOBAL).run({"a": [{"f": 0}]}) == {
        "output": [{"f": 1}]
    }
    assert e.use("a", "a", replace=ReplacingScope.GLOBAL).run(
        {"a": {"f": 0, "b": 1}, "b": 1}
    ) == {
        "a": {"f": 1}
    }
    assert e.use("a", "a", replace=ReplacingScope.GLOBAL).run({"a": [{"f": 0}], "b": 1}) == {
        "a": [{"f": 1}],
    }