from typing import Any, Dict
from enum import Enum

from pydantic import BaseModel

from implementation.apis.google_cloud.schema import (
    GoogleCloudClientConfig,
)

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
    service: str="sheets"
    version: str="v4"


class Dimension(Enum):
    ROWS = 'ROWS'
    COLUMNS = 'COLUMNS'


class InputOption(Enum):
    RAW = 'RAW'
    USER_ENTERED = 'USER_ENTERED'


class InsertDataOption(Enum):
    INSERT_ROWS = 'INSERT_ROWS'
    OVERWRITE = 'OVERWRITE'