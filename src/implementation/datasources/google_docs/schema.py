from implementation.apis.google_cloud.schema import (
    GoogleCloudClientConfig,
)

class GoogleDocsClientConfig(GoogleCloudClientConfig):
    scopes: list[str] = [
        "https://www.googleapis.com/auth/documents" ##################################################
    ]
    service: str = "docs"
    version: str = "v1"