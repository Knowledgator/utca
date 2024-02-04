from __future__ import annotations
from typing import Optional, Any, cast, Dict, Union, Generic, TypeVar
from enum import Enum

from pydantic import BaseModel

from core.datasource_level.schema import DatasourceAction
from implementation.datasources.google_spreadsheet.schema import (
    Sheet
)

class GoogleSpreadsheetSelectRange(BaseModel):
    page_name: Optional[str]=None
    select_range: Optional[str]=None

    @property
    def cells_range(self) -> str:
        if not (self.page_name or self.select_range):
            raise ValueError(f'page_name or select_range should be provided')
        return '!'.join((i for i in (self.page_name, self.select_range) if i))


class Dimension(Enum):
    ROWS = 'ROWS'
    COLUMNS = 'COLUMNS'


class GoogleSpreadsheetWriteRange(BaseModel):
    page_name: Optional[str]=None
    select_range: Optional[str]=None
    values: list[list[str]]
    dimension: Dimension = Dimension.ROWS

    @property
    def cells_range(self) -> Dict[str, Any]:
        if not (self.page_name or self.select_range):
            raise ValueError(f'page_name or select_range should be provided')
        return {
            'range': '!'.join((i for i in (self.page_name, self.select_range) if i)),
            'values': self.values,
            'majorDimension': self.dimension.value,
            
        }


RangeType = TypeVar('RangeType', GoogleSpreadsheetSelectRange, GoogleSpreadsheetWriteRange)


class Range(BaseModel, Generic[RangeType]):
    select_range: RangeType

    @property
    def cells_range(self) -> Union[str, Dict[str, Any]]:
        return self.select_range.cells_range
    

class Ranges(BaseModel, Generic[RangeType]):
    select_range: list[RangeType]

    @property
    def cells_range(self) -> list[Union[str, Dict[str, Any]]]:
        return [r.cells_range for r in self.select_range]


class InputOption(Enum):
    RAW = 'RAW'
    USER_ENTERED = 'USER_ENTERED'


class GoogleSpreadsheetRead(DatasourceAction, Range[GoogleSpreadsheetSelectRange]):
    spreadsheet_id: str
    dimension: Dimension = Dimension.ROWS

    def execute(self, sheet_service) -> Dict[str, Any]: # type: ignore
        try:
            result = ( # type: ignore
                sheet_service.values() # type: ignore
                .get(
                    spreadsheetId=self.spreadsheet_id, 
                    range=self.select_range.cells_range,
                    majorDimension=self.dimension.value
                )
                .execute() 
            )
            return {'table': result.get("values", [])} # type: ignore
        except Exception as e:
            raise ValueError(f'Unable to read specified sheet: {e}')


class GoogleSpreadsheetReadBatch(DatasourceAction, Ranges[GoogleSpreadsheetSelectRange]):
    spreadsheet_id: str
    dimension: Dimension = Dimension.ROWS

    def execute(self, sheet_service) -> Dict[str, Any]: # type: ignore
        try:
            result = ( # type: ignore
                sheet_service.values() # type: ignore
                .batchGet(
                    spreadsheetId=self.spreadsheet_id, 
                    ranges=self.cells_range,
                    majorDimension=self.dimension.value,
                )
                .execute() 
            )
            return {
                'tables': [i.get("values", []) for i in result.get("valueRanges", [])]  # type: ignore
            }
        except Exception as e:
            raise ValueError(f'Unable to read specified sheet: {e}')


class GoogleSpreadsheetUpdate(DatasourceAction, Range[GoogleSpreadsheetWriteRange]):
    spreadsheet_id: str
    value_input_option: InputOption = InputOption.USER_ENTERED

    def execute(self, sheet_service) -> Dict[str, Any]: # type: ignore
        update = cast(Dict[str, Any], self.cells_range)
        try:
            (
                sheet_service # type: ignore
                .values()
                .update(
                    spreadsheetId=self.spreadsheet_id,
                    valueInputOption=self.value_input_option.value,
                    body=update,
                    range=update['range']
                )
                .execute()
            )
            return {}
        except Exception as e:
            raise ValueError(f"An error occurred: {e}")


class GoogleSpreadsheetUpdateBatch(DatasourceAction, Ranges[GoogleSpreadsheetWriteRange]):
    spreadsheet_id: str
    value_input_option: InputOption = InputOption.USER_ENTERED

    def execute(self, sheet_service) -> Dict[str, Any]: # type: ignore
        try:
            (
                sheet_service # type: ignore
                .values()
                .batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body={
                        "data": self.cells_range,
                        "valueInputOption": self.value_input_option.value,
                    },
                )
                .execute()
            )
            return {}
        except Exception as e:
            raise ValueError(f"An error occurred: {e}")


class InsertDataOption(Enum):
    INSERT_ROWS = 'INSERT_ROWS'
    OVERWRITE = 'OVERWRITE'


class GoogleSpreadsheetAppend(DatasourceAction, Range[GoogleSpreadsheetWriteRange]):
    spreadsheet_id: str
    value_input_option: InputOption = InputOption.USER_ENTERED
    insert_data_option: InsertDataOption = InsertDataOption.OVERWRITE

    def execute(self, sheet_service) -> Dict[str, Any]: # type: ignore
        update = cast(Dict[str, Any], self.cells_range)
        try:
            (
                sheet_service # type: ignore
                .values()
                .append(
                    spreadsheetId=self.spreadsheet_id,
                    valueInputOption=self.value_input_option.value,
                    body=update,
                    range=update['range']
                )
                .execute()
            )
            return {}
        except Exception as e:
            raise ValueError(f"An error occurred: {e}")
        

class GoogleSpreadsheetCreate(DatasourceAction):
    title: str
    sheets: Optional[list[Sheet]] = None

    def execute(self, sheet_service) -> Dict[str, Any]: # type: ignore
        try:
            idx: str = ( # type: ignore
                sheet_service # type: ignore
                .create( 
                    body={
                        'properties': {
                            'title': self.title
                        },
                        'sheets': [
                            s.info for s in self.sheets
                        ] if self.sheets else []
                    }, 
                    fields='spreadsheetId'
                )
                .execute()
                .get('spreadsheetId')
            )
            return {
                'spread_sheet_id': idx # type: ignore
            }
        except Exception as e:
            raise ValueError(f'Unable to create sheet: {e}')