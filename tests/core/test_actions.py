from typing import Dict, List
import copy
import logging
import io

from utca.core import (
    Evaluator, 
    Flush, 
    Log,
    AddData,
    RenameAttribute,
    RenameAttributeQuery,
    SetValue,
    UnpackValue,
    NestToKey,
    ExecuteFunction,
    ReplacingScope,
)

def test_flush_root_all():
    input_data = {
        "a": 1,
        "b": 2
    }

    res = Flush().run(input_data)
    assert res == {}


def test_flush_root_specific():
    input_data = {
        "a": 1,
        "b": 2
    }

    res = Flush(
        keys=["a"], name="hi"
    ).run(input_data)
    assert res == {"b": 2}


def test_flush_nested_all():
    input_data = {
        "a": {
            "c": 1,
            "d": 2
        },
        "b": 2
    }

    res = Flush().use(get_key="a", set_key="a").run(input_data)
    assert res == {"a": {}, "b": 2}

    res = Flush().use(get_key="a", set_key="b").run(input_data)
    assert res == {"a": {}, "b": {}}


def test_flush_nested_specific():
    input_data = {
        "a": {
            "c": 1,
            "d": 2
        },
        "b": 2
    }

    res = Flush(keys=["c"]).use(get_key="a", set_key="a").run(copy.deepcopy(input_data))
    assert res == {"a": {"d": 2}, "b": 2}

    res = Flush(keys=["c"]).use(get_key="a", set_key="b").run(input_data)
    assert res == {"a": {"c": 1, "d": 2}, "b": {"d": 2}}


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


def test_add_data():
    a = AddData({"a": 1})
    inputs = {"b": 2, "c": {"d": 1}}

    res = a.run(copy.copy(inputs))
    assert res == {"a": 1, "b": 2, "c": {"d": 1}}

    res = a.use(get_key="c").run(copy.copy(inputs))
    assert res == {
        "a": 1,
        "b": 2, 
        "c": {
            "d": 1
        },
        "d": 1,
    }
    res = a.use(get_key="c", set_key="c").run(inputs)
    assert res == {
        "b": 2, 
        "c": {
            "a": 1,
            "d": 1
        },
    }


def test_rename_attribute():
    r = RenameAttribute("a", "b")

    assert r.run({"a": 1}) == {"b": 1}
    assert r.use("b").run({"b": {"a": 1}}) == {"b": 1}
    assert r.use("b", "b").run({"b": {"a": 1}}) == {"b": {"b": 1}}


def test_rename_query_attribute():
    r = RenameAttributeQuery("A<-a;B<-b")

    assert r.run({"a": 1, "b": 2}) == {"A": 1, "B": 2}

    r = RenameAttributeQuery("b<-a")

    assert r.use("b").run({"b": {"a": 1}}) == {"b": 1}
    assert r.use("b", "b").run({"b": {"a": 1}}) == {"b": {"b": 1}}

    try:
        r = RenameAttributeQuery("A<-aB<-b")
        raise Exception("Should throw error!") 
    except Exception as e:
        logging.info(e)


def test_set_value():
    s = SetValue("a", 1)

    assert s.run({"a": 1}) == {"a": 1}
    assert s.run({"b": 1}) == {"a": 1, "b": 1}
    assert s.use("a").run({"a": {"a": 1}}) == {"a": 1}
    assert s.use("a", "a").run({"a": {}}) == {"a": {"a": 1}}


def test_unpack_value():
    u = UnpackValue("a")

    assert u.run({"a": {"b": 1, "c": 2}}) == {"b": 1, "c": 2}
    assert u.use("c").run({
        "c": {
            "b": 1, 
            "a": {"d": 1}
        }
    }) == {
        "d": 1,
        "b": 1
    }
    assert u.use("c", "c").run({
        "c": {
            "b": 1, 
            "a": {
                "d": 1
            }
        }
    }) == {
        "c": {
            "b": 1,
            "d": 1,
        }
    }


def test_nest_to_key():
    n = NestToKey("a")

    assert n.run({"b": 1}) == {"a": {"b": 1}}
    assert n.use("c").run({
        "c": {"b": 1}
    }) == {
        "a": {"b": 1}
    }
    assert n.use("c", "c").run({
        "c": {"b": 1}
    }) == {
        "c": {"a": {"b": 1}}
    }


def test_execute_function():
    def f(a: Dict[str, int]) -> Dict[str, int]:
        a["a"] += 1
        return a
    
    def fs(a: Dict[str, int]) -> List[Dict[str, int]]:
        a["a"] += 1
        return [a] * 2
    
    e = ExecuteFunction(f)
    es = ExecuteFunction(fs)

    assert e.run({"a": 0})["a"] == 1
    assert es.run({"a": 0})["output"][0]["a"] == 1
    
    assert e.use("c").run({"c": {"a": 0}}) == {
        "c": {"a": 0},
        "a": 1
    }
    assert es.use("c").run({"c": {"a": 0}}) == {
        "c": {"a": 0},
        "output": [{"a": 1}]*2
    }

    assert e.use("c", "c").run({"c": {"a": 0}}) == {
        "c": {"a": 1}
    }
    assert es.use("c", "c").run({"c": {"a": 0}}) == {
        "c": [{"a": 1}]*2
    }


def test_actions_replacing_scopes_and_default_key():
    def f(a: Dict[str, int]) -> Dict[str, int]:
        return {
            "a": a["a"] + 1
        }
    
    def fs(a: Dict[str, int]) -> List[Dict[str, int]]:
        a["a"] += 1
        return [a] * 2
    
    e = ExecuteFunction(f, replace=ReplacingScope.LOCAL)
    es = ExecuteFunction(fs, default_key="test", replace=ReplacingScope.LOCAL)

    # test LOCAL
    assert e.run({"a": 0, "b": 1}) == {"a": 1}
    assert es.run({"a": 0}) == {"a": 0, "test": [{"a": 1}, {"a": 1}]}
    
    assert e.use("c").run({"c": {"a": 0}, "b": 1}) == {
        "a": 1
    }
    assert es.use("c").run({"c": {"a": 0}}) == {
        "c": {"a": 0},
        "test": [{"a": 1}]*2
    }

    assert e.use("c", "c").run({"c": {"a": 0}, "b": 1}) == {
        "c": {"a": 1},
        "b": 1
    }
    assert es.use("c", "c").run({"c": {"a": 0}, "b": 1}) == {
        "c": [{"a": 1}]*2,
        "b": 1
    }

    # test GLOBAL
    assert e.use(replace=ReplacingScope.GLOBAL).run({"a": 0, "b": 1}) == {"a": 1}
    assert es.use(replace=ReplacingScope.GLOBAL).run({"a": 0}) == {
        "test": [{"a": 1}, {"a": 1}]
    }
    
    assert e.use("c", replace=ReplacingScope.GLOBAL).run({"c": {"a": 0}, "b": 1}) == {
        "a": 1
    }
    assert es.use("c", replace=ReplacingScope.GLOBAL).run({"c": {"a": 0}}) == {
        "test": [{"a": 1}]*2
    }

    assert e.use("c", "c", replace=ReplacingScope.GLOBAL).run({"c": {"a": 0}, "b": 1}) == {
        "c": {"a": 1},
    }
    assert es.use("c", "c", replace=ReplacingScope.GLOBAL).run({"c": {"a": 0}, "b": 1}) == {
        "c": [{"a": 1}]*2,
    }
