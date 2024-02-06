from typing import Any, Dict

# from pydantic import BaseModel

from core.datasource_level.schema import (
    DatasourceInput,
    DatasourceOutput
)
from implementation.apis.google_cloud.schema import (
    GoogleCloudClientConfig,
    GoogleCloudDatasourceServiceConfig,
)

class GoogleDocsClientConfig(GoogleCloudClientConfig):
    scopes: list[str] = [
        "https://www.googleapis.com/auth/documents" ##################################################
    ]


class GoogleDocsReadConfig(GoogleCloudDatasourceServiceConfig):
    ...


class GoogleDocsReadInput(DatasourceInput):
    document_id: str


class GoogleDocsReadOutput(DatasourceOutput):
    title: str
    body: Dict[str, Any]

class GoogleDocsWriteConfig(GoogleCloudDatasourceServiceConfig):
    document_id: str


class GoogleDocsWriteInput(DatasourceInput):
    action: Dict[str, Any]


class GoogleDocsWriteOutput(DatasourceOutput):
    ...


class GoogleDocsCreateConfig(GoogleCloudDatasourceServiceConfig):
    ...


class GoogleDocsCreateInput(DatasourceInput):
    title: str


class GoogleDocsCreateOutput(DatasourceOutput):
    document_id: str
