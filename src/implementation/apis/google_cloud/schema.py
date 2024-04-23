from typing import Any, Dict, Optional, Union

from pydantic import BaseModel

class GoogleCloudClientConfig(BaseModel):
    """
    Google Cloud client configuration
    """
    credentials: Optional[Union[Dict[str, Any], str]]=None
    """
    Credentials for authorization
    """
    scopes: list[str]
    """
    Access scopes
    """
    service: str
    """
    Service name
    """
    version: str
    """
    API version
    """