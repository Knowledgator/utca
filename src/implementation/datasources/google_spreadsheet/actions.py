from __future__ import annotations
from typing import Any, Dict, List, cast

from core.executable_level_1.actions import Action
from implementation.apis.google_cloud.client import (
    GoogleCloudClient
)
from implementation.datasources.google_spreadsheet.schema import (
    Dimension,
    InputOption,
    InsertDataOption
)


class GoogleSpreadsheetAction(Action):
    def __init__(self, client: GoogleCloudClient) -> None:
        self.sheet_service = client.service.spreadsheets()


class GoogleSpreadsheetRead(GoogleSpreadsheetAction):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = cast(Dict[str, Any], (
                self.sheet_service.values() # type: ignore
                .get(
                    spreadsheetId=input_data["spreadsheet_id"], 
                    range=input_data["cells_range"],
                    majorDimension=input_data.get("dimension", Dimension.ROWS).value
                )
                .execute() 
            ))
            input_data["table"] = result.get("values", [])
            return input_data
        except Exception as e:
            raise ValueError(f"Unable to read specified sheet: {e}")


class GoogleSpreadsheetReadBatch(GoogleSpreadsheetAction):
    def execute(self, input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            result = cast(Dict[str, Any], (
                self.sheet_service.values() # type: ignore
                .batchGet(
                    spreadsheetId=input_data["spreadsheet_id"],
                    ranges=input_data["cells_ranges"],
                    majorDimension=input_data.get("dimension", Dimension.ROWS).value,
                )
                .execute() 
            ))
            return [
                {"table": i.get("values", [])}
                for i in cast(List[Dict[str, List[Any]]], result.get("valueRanges", []))
            ]
        except Exception as e:
            raise ValueError(f"Unable to read specified sheet: {e}")


class GoogleSpreadsheetWrite(GoogleSpreadsheetAction):
   def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            input_data["spreadsheet"] = (
                self.sheet_service # type: ignore
                .values()
                .update(
                    spreadsheetId=input_data["spreadsheet_id"],
                    valueInputOption=input_data.get(
                        "value_input_option", InputOption.USER_ENTERED
                    ).value,
                    body={
                        "values": input_data["table"],
                        "majorDimension": input_data.get(
                            "dimension", Dimension.ROWS
                        ).value,
                    },
                    range=input_data["cells_range"]
                )
                .execute()
            )
            return input_data
        except Exception as e:
            raise ValueError(f"An error occurred: {e}")


class GoogleSpreadsheetWriteBatch(GoogleSpreadsheetAction):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            input_data["spreadsheet"] = (
                self.sheet_service # type: ignore
                .values()
                .batchUpdate(
                    spreadsheetId=input_data["spreadsheet_id"],
                    body={
                        "data": input_data["inputs"],
                        "valueInputOption": input_data.get(
                            "value_input_option", InputOption.USER_ENTERED
                        ).value,
                    },
                )
                .execute()
            )
            return input_data
        except Exception as e:
            raise ValueError(f"An error occurred: {e}")


class GoogleSpreadsheetAppend(GoogleSpreadsheetAction):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            (
                self.sheet_service # type: ignore
                .values()
                .append(
                    spreadsheetId=input_data["spreadsheet_id"],
                    valueInputOption=input_data.get(
                        "value_input_option", InputOption.USER_ENTERED
                    ).value,
                    insertDataOption=input_data.get(
                        "insert_data_option", InsertDataOption.OVERWRITE
                    ).value,
                    body={
                        "values": input_data["table"],
                        "majorDimension": input_data.get(
                            "dimension", Dimension.ROWS
                        ).value,
                    },
                    range=input_data["cells_range"]
                )
                .execute()
            )
            return {}
        except Exception as e:
            raise ValueError(f"An error occurred: {e}")


class GoogleSpreadsheetCreate(GoogleSpreadsheetAction):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            input_data["spreadsheet_id"] = (
                self.sheet_service
                .create( 
                    body={
                        "properties": {
                            "title": input_data["title"]
                        },
                        "sheets": input_data.get("sheets", ["Sheet1"])
                    }, 
                    fields="spreadsheetId"
                )
                .execute()
                .get("spreadsheetId")
            )
            return input_data
        except Exception as e:
            raise ValueError(f"Unable to create sheet: {e}")