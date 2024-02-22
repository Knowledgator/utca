from typing import Any, Dict, Union

from pydantic import BaseModel

class GoogleCloudClientConfig(BaseModel):
    credentials: Union[Dict[str, Any], str, None]
    scopes: list[str]
    service: str
    version: str