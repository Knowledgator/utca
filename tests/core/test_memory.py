from utca.core import (
    Evaluator,
    GetMemory,
    SetMemory,
    DeleteMemory,
    MemoryGetInstruction,
    MemorySetInstruction,
    MemoryManager,
)

def test_get_memory():
    m = MemoryManager(initial_data={"test": "OK"})
    res = Evaluator(
        schema=GetMemory(["test"], memory_instruction=MemoryGetInstruction.GET),
        memory_manager=m
    ).run()
    assert res["test"] == "OK"
    assert m.memory.memory["test"] == "OK"
    
    res = Evaluator(
        schema=GetMemory(["test"], memory_instruction=MemoryGetInstruction.POP),
        memory_manager=m
    ).run()
    assert res["test"] == "OK"
    assert m.memory.memory.get("test") is None


def test_set_memory():
    m = MemoryManager(initial_data={"else": "data"})

    res = Evaluator(
        schema=SetMemory("test", "data", MemorySetInstruction.SET),
        memory_manager=m
    ).run({"data": "OK"})
    assert res["data"] == "OK"
    assert m.memory.memory["test"] == "OK"
    assert m.memory.memory["else"] == "data"
    
    res = Evaluator(
        schema=SetMemory("test", "other", MemorySetInstruction.MOVE),
        memory_manager=m
    ).run({"other": "Nice"})
    assert res.get("other") is None
    assert m.memory.memory["test"] == "Nice"
    assert m.memory.memory["else"] == "data"


def test_delete_memory():
    m = MemoryManager(initial_data={"test1": "OK", "test2": "OK"})

    res = Evaluator(
        schema=DeleteMemory(["test1"]),
        memory_manager=m
    ).run({"data": "OK"})
    assert res["data"] == "OK"
    assert m.memory.memory.get("test1") is None
    assert m.memory.memory["test2"] == "OK"
    
    m = MemoryManager(initial_data={"test1": "OK", "test2": "OK"})

    res = Evaluator(
        schema=DeleteMemory(),
        memory_manager=m
    ).run({"data": "OK"})
    assert res.get("other") is None
    assert res["data"] == "OK"
    assert m.memory.memory.get("test1") is None
    assert m.memory.memory.get("test2") is None