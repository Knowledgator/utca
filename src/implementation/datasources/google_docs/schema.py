from typing import Any, Dict, Optional

# from pydantic import BaseModel

from core.datasource_level.schema import DatasourceData
from implementation.datasources.google_cloud.schema import GoogleCloudClientConfig

# class GoogleSpreadsheetPage(BaseModel):
#     table: list[list[Any]]


# class Sheet(BaseModel):
#     title: str

#     @property
#     def info(self) -> Dict[str, Any]:
#         return {
#             'properyties': {
#                 'title': self.title
#             }
#         }


class GoogleDocsClientConfig(GoogleCloudClientConfig):
    scopes: list[str] = [
        "https://www.googleapis.com/auth/documents" ##################################################
    ]


class GoogleDocsData(DatasourceData):
    title: Optional[str] = None
    body: Optional[Dict[str, Any]] = None