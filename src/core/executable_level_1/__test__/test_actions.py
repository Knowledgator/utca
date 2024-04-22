import copy
import logging
import io

from core import (
    Evaluator, 
    EvaluatorConfigs,
    Flush, 
    Log,
    AddData,
    RenameAttribute,
    RenameAttributeQuery,
    SetValue,
    UnpackValue,
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
        EvaluatorConfigs(
            "TestEvaluator",
            logging_level=logging.INFO,
            logging_handler=logging.StreamHandler(stream)
        )
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
        "c": {
            "b": 1,
            "a": {"d": 1},
        },
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