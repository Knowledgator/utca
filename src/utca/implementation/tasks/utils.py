from typing import Any, Dict

def ensure_attributes(data: Dict[str, Any], key: str="output") -> object:
    class Wrapper:
        def __init__(self, data: Dict[str, Any]):
            self.__dict__ = data
    return Wrapper(data)