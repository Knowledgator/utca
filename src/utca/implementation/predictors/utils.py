from typing import Any, Dict, cast

def ensure_dict(data: Any, key: str="output") -> Dict[str, Any]:
    if not isinstance(data, Dict):
        return {
            key: data
        }
    return cast(Dict[str, Any], data)