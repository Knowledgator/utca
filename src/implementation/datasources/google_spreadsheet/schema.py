from typing import Any, Dict, Optional

from pydantic import BaseModel

from core.datasource_level.schema import DatasourceData
from implementation.datasources.google_cloud.schema import GoogleCloudClientConfig

class GoogleSpreadsheetPage(BaseModel):
    table: list[list[Any]]


class Sheet(BaseModel):
    title: str

    @property
    def info(self) -> Dict[str, Any]:
        return {
            'properyties': {
                'title': self.title
            }
        }


class GoogleSpreadsheetClientConfig(GoogleCloudClientConfig):
    scopes: list[str] = [
        "https://www.googleapis.com/auth/spreadsheets" ##################################################
    ]


class GoogleSpreadsheetData(DatasourceData):
    spread_sheet_id: Optional[str]=None
    table: Optional[list[list[Any]]]=None
    tables: Optional[list[list[list[Any]]]]=None
