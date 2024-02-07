from __future__ import annotations
from typing import Any, Dict, Type

from core.datasource_level_2.datasource import DatasourceAction
from implementation.datasources.google_spreadsheet.schema import (
    GoogleSpreadsheetReadConfig,
    GoogleSpreadsheetReadInput, 
    GoogleSpreadsheetReadOutput,
    GoogleSpreadsheetWriteConfig,
    GoogleSpreadsheetWriteInput,
    GoogleSpreadsheetWriteOutput,
    GoogleSpreadsheetAppendConfig,
    GoogleSpreadsheetCreateConfig,
    GoogleSpreadsheetCreateInput,
    GoogleSpreadsheetCreateOutput
)

class GoogleSpreadsheetRead(
    DatasourceAction[
        GoogleSpreadsheetReadConfig, 
        GoogleSpreadsheetReadInput, 
        GoogleSpreadsheetReadOutput
    ]
):
    input_class: Type[GoogleSpreadsheetReadInput] = GoogleSpreadsheetReadInput
    output_class: Type[GoogleSpreadsheetReadOutput] = GoogleSpreadsheetReadOutput

    def invoke(self, input_data: GoogleSpreadsheetReadInput) -> Dict[str, Any]:
        try:
            result = ( # type: ignore
                self.cfg.service.values() # type: ignore
                .get(
                    spreadsheetId=self.cfg.spreadsheet_id, 
                    range=input_data.cells_range,
                    majorDimension=self.cfg.dimension.value
                )
                .execute() 
            )
            return {'table': result.get("values", [])} # type: ignore
        except Exception as e:
            raise ValueError(f'Unable to read specified sheet: {e}')


    def invoke_batch(self, input_data: list[GoogleSpreadsheetReadInput]) -> list[Dict[str, Any]]:
        try:
            result = ( # type: ignore
                self.cfg.service.values() # type: ignore
                .batchGet(
                    spreadsheetId=self.cfg.spreadsheet_id, 
                    ranges=[i.cells_range for i in input_data],
                    majorDimension=self.cfg.dimension.value,
                )
                .execute() 
            )
            return [
                {'table': i.get("values", [])} # type: ignore
                for i in result.get("valueRanges", []) # type: ignore
            ]
        except Exception as e:
            raise ValueError(f'Unable to read specified sheet: {e}')


class GoogleSpreadsheetWrite(
    DatasourceAction[
        GoogleSpreadsheetWriteConfig, 
        GoogleSpreadsheetWriteInput, 
        GoogleSpreadsheetWriteOutput
    ]
):
    input_class: Type[GoogleSpreadsheetWriteInput] = GoogleSpreadsheetWriteInput
    output_class: Type[GoogleSpreadsheetWriteOutput] = GoogleSpreadsheetWriteOutput

    def invoke(self, input_data: GoogleSpreadsheetWriteInput) -> Dict[str, Any]:
        update: Dict[str, Any] = input_data.cells_range
        try:
            (
                self.cfg.service # type: ignore
                .values()
                .update(
                    spreadsheetId=self.cfg.spreadsheet_id,
                    valueInputOption=self.cfg.value_input_option.value,
                    body=update,
                    range=update['range']
                )
                .execute()
            )
            return {}
        except Exception as e:
            raise ValueError(f"An error occurred: {e}")


    def invoke_batch(self, input_data: list[GoogleSpreadsheetWriteInput]) -> list[Dict[str, Any]]:
        try:
            (
                self.cfg.service # type: ignore
                .values()
                .batchUpdate(
                    spreadsheetId=self.cfg.spreadsheet_id,
                    body={
                        "data": [i.cells_range for i in input_data],
                        "valueInputOption": self.cfg.value_input_option.value,
                    },
                )
                .execute()
            )
            return []
        except Exception as e:
            raise ValueError(f"An error occurred: {e}")


class GoogleSpreadsheetAppend(
    DatasourceAction[
        GoogleSpreadsheetAppendConfig, 
        GoogleSpreadsheetWriteInput, 
        GoogleSpreadsheetWriteOutput
    ], 
):
    input_class: Type[GoogleSpreadsheetWriteInput] = GoogleSpreadsheetWriteInput
    output_class: Type[GoogleSpreadsheetWriteOutput] = GoogleSpreadsheetWriteOutput

    def invoke(self, input_data: GoogleSpreadsheetWriteInput) -> Dict[str, Any]:
        update = input_data.cells_range
        try:
            (
                self.cfg.service # type: ignore
                .values()
                .append(
                    spreadsheetId=self.cfg.spreadsheet_id,
                    valueInputOption=self.cfg.value_input_option.value,
                    body=update,
                    range=update['range']
                )
                .execute()
            )
            return {}
        except Exception as e:
            raise ValueError(f"An error occurred: {e}")
        
    
    def invoke_batch(self, input_data: list[GoogleSpreadsheetWriteInput]) -> list[Dict[str, Any]]:
        raise Exception("Not supported")


class GoogleSpreadsheetCreate(
    DatasourceAction[
        GoogleSpreadsheetCreateConfig, 
        GoogleSpreadsheetCreateInput, 
        GoogleSpreadsheetCreateOutput
    ]
):
    input_class: Type[GoogleSpreadsheetCreateInput] = GoogleSpreadsheetCreateInput
    output_class: Type[GoogleSpreadsheetCreateOutput] = GoogleSpreadsheetCreateOutput

    def invoke(self, input_data: GoogleSpreadsheetCreateInput) -> Dict[str, Any]:
        try:
            idx: str = ( # type: ignore
                self.cfg.service # type: ignore
                .create( 
                    body={
                        'properties': {
                            'title': input_data.title
                        },
                        'sheets': [
                            s.info for s in input_data.sheets
                        ] if input_data.sheets else []
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
        
    
    def invoke_batch(self, input_data: list[GoogleSpreadsheetCreateInput]) -> list[Dict[str, Any]]:
        raise Exception("Not supported")