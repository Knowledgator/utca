from typing import Any, Dict, cast

def ensure_dict(data: Any) -> Dict[str, Any]:
    if not isinstance(data, Dict):
        return {
            "output": data
        }
    return cast(Dict[str, Any], data)