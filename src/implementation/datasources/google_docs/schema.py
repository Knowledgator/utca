from implementation.apis.google_cloud.schema import (
    GoogleCloudClientConfig,
)

class GoogleDocsClientConfig(GoogleCloudClientConfig):
    """
    Google Documents default configuration
    """
    scopes: list[str] = [
        "https://www.googleapis.com/auth/documents"
    ]
    """
    Read and write acess to all documents
    """
    service: str = "docs"
    """
    Google Documents service
    """
    version: str = "v1"
    """
    API version
    """