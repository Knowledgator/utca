from typing import Any, Dict, Optional
from enum import Enum

from pydantic import BaseModel

from core.datasource_level_2.schema import DatasourceInput, DatasourceOutput
from implementation.apis.google_cloud.schema import (
    GoogleCloudClientConfig,
    GoogleCloudDatasourceServiceConfig
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


class Dimension(Enum):
    ROWS = 'ROWS'
    COLUMNS = 'COLUMNS'


class InputOption(Enum):
    RAW = 'RAW'
    USER_ENTERED = 'USER_ENTERED'


class InsertDataOption(Enum):
    INSERT_ROWS = 'INSERT_ROWS'
    OVERWRITE = 'OVERWRITE'


class GoogleSpreadsheetReadConfig(GoogleCloudDatasourceServiceConfig):
    spreadsheet_id: str
    dimension: Dimension = Dimension.ROWS


class GoogleSpreadsheetReadInput(DatasourceInput):
    sheet_name: Optional[str]=None
    select_range: Optional[str]=None

    @property
    def cells_range(self) -> str:
        if not (self.sheet_name or self.select_range):
            raise ValueError(f'page_name or select_range should be provided')
        return '!'.join((i for i in (self.sheet_name, self.select_range) if i))


class GoogleSpreadsheetReadOutput(DatasourceOutput):
    table: list[list[Any]]


class GoogleSpreadsheetWriteConfig(GoogleCloudDatasourceServiceConfig):
    spreadsheet_id: str
    value_input_option: InputOption = InputOption.USER_ENTERED


class GoogleSpreadsheetWriteInput(DatasourceInput):
    sheet_name: Optional[str]=None
    select_range: Optional[str]=None
    table: list[list[str]]
    dimension: Dimension = Dimension.ROWS

    @property
    def cells_range(self) -> Dict[str, Any]:
        if not (self.sheet_name or self.select_range):
            raise ValueError(f'page_name or select_range should be provided')
        return {
            'range': '!'.join((i for i in (self.sheet_name, self.select_range) if i)),
            'values': self.table,
            'majorDimension': self.dimension.value,
            
        }


class GoogleSpreadsheetWriteOutput(DatasourceOutput):
    ...


class GoogleSpreadsheetAppendConfig(GoogleSpreadsheetWriteConfig):
    insert_data_option: InsertDataOption = InsertDataOption.OVERWRITE


class GoogleSpreadsheetCreateConfig(GoogleCloudDatasourceServiceConfig):
    ...


class GoogleSpreadsheetCreateInput(DatasourceInput):
    title: str
    sheets: Optional[list[Sheet]] = None


class GoogleSpreadsheetCreateOutput(DatasourceOutput):
    spreadsheet_id: str