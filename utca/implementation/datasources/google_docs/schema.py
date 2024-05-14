from typing import List

from utca.implementation.apis.google_cloud.schema import (
    GoogleCloudClientConfig,
)

class GoogleDocsClientConfig(GoogleCloudClientConfig):
    """
    Google Documents default configuration

    Arguments:
        scopes (List[str]): Access scopes. Defaults to 
            ["https://www.googleapis.com/auth/documents"] 
            (Read and write acess to all documents).
        
        service (str): Service name. Defaults to "docs" (Google Documents service).
        
        version (str): API version. Defaults to "v1".
    """
    scopes: List[str] = [
        "https://www.googleapis.com/auth/documents"
    ]
    service: str = "docs"
    version: str = "v1"