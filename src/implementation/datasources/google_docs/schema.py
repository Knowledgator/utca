from typing import Any, Dict, Optional

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
    title: Optional[str] = None
    body: Optional[Dict[str, Any]] = None


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
    doc_id: str
