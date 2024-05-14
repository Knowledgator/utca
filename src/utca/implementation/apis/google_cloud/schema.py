from typing import Any, Dict, List, Optional, Union

from utca.core.executable_level_1.schema import Config

class GoogleCloudClientConfig(Config):
    """
    Google Cloud client configuration

    Args:
        credentials (Optional[Union[Dict[str, Any], str]], optional): Credentials 
            for authorization. If None, environment credentials will be used. 
            Defaults to None.
        
        scopes (List[str]): Access scopes.
        
        service (str): Service name.
        
        version (str): API version.
    """
    credentials: Optional[Union[Dict[str, Any], str]]=None
    scopes: List[str]
    service: str
    version: str