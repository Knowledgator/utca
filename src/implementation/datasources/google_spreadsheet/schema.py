from typing import Any, Dict, Union, Optional

from pydantic import BaseModel

from core.datasource_level.schema import DatasourceConfig, DatasourceData

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


class GoogleSpreadsheetClientConfig(DatasourceConfig):
    credentials: Union[Dict[str, Any], str]
    scopes: list[str] = [
        "https://www.googleapis.com/auth/spreadsheets" ##################################################
    ]


class GoogleSpreadsheetData(DatasourceData):
    spread_sheet_id: Optional[str]=None
    table: Optional[list[list[Any]]]=None
    tables: Optional[list[list[list[Any]]]]=None
