from __future__ import annotations
from typing import Any, Dict, List, Optional, cast

from utca.core.executable_level_1.actions import (
    Action, ActionInput, ActionOutput
)
from utca.implementation.apis.google_cloud.client import (
    GoogleCloudClient
)
from utca.implementation.datasources.google_sheets.schema import (
    Dimension,
    InputOption,
    InsertDataOption
)


class GoogleSheetsAction(Action[ActionInput, ActionOutput]):
    """
    Base Google Spreadsheets action
    """
    def __init__(
        self, 
        client: GoogleCloudClient,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            client (GoogleCloudClient): Google client that will be used for access.

            name (Optional[str], optional): name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.sheet_service = client.service.spreadsheets()


class GoogleSheetsRead(GoogleSheetsAction[Dict[str, Any], Dict[str, Any]]):
    """
    Read spreadsheet
    """
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "spreadsheet_id" (str): Spreadsheet ID (can be found
                    in url: https://docs.google.com/spreadsheets/d/***spreadsheet_id***/edit#gid=0);

                "cells_range" (str): Range of cells provided in A1 notation.
                    Examples: "B2:C2", "A1", "Sheet1", "Sheet1!A1:B1", etc..

                "dimension" (Dimension, optional): Reading dimension. May be 
                    Dimension.ROWS or Dimension.COLUMNS. Defaults to Dimension.ROWS.

        Raises:
            Exception: If unable to read spreadsheet.

        Returns:
            Dict[str, Any]: Expected keys:
                "table" (List[List[Any]]): Table that represents sheet or part of
                    it specified by "cells_range";
        """
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
            return {
                "table": result.get("values", [])
            }
        except Exception as e:
            raise Exception(f"Unable to read spreadsheet: {e}")


class GoogleSheetsReadBatch(GoogleSheetsAction[Dict[str, Any], List[Dict[str, Any]]]):
    """
    Read spreadsheet batch
    """
    def execute(self, input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "spreadsheet_id" (str): Spreadsheet ID (can be found
                    in url: https://docs.google.com/spreadsheets/d/***spreadsheet_id***/edit#gid=0);

                "cells_ranges" (List[str]): Ranges of cells provided in A1 notation.
                    Examples: "B2:C2", "A1", "Sheet1", "Sheet1!A1:B1", etc..

                "dimension" (Dimension, optional): Reading dimension. May be 
                    Dimension.ROWS or Dimension.COLUMNS. Defaults to Dimension.ROWS.

        Raises:
            Exception: If unable to read spreadsheet.

        Returns:
            List[Dict[str, Any]]: Each object in list expected to contain:
                "table" (List[List[Any]]): Table that represents sheet or part of
                    it specified by corresponding range in "cells_ranges";
        """
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
            raise Exception(f"Unable to read spreadsheet: {e}")


class GoogleSheetsWrite(GoogleSheetsAction[Dict[str, Any], Dict[str, Any]]):
   """
   Write to spreadsheet
   """
   def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "spreadsheet_id" (str): Spreadsheet ID (can be found
                    in url: https://docs.google.com/spreadsheets/d/***spreadsheet_id***/edit#gid=0);

                "cells_range" (str): Range of cells provided in A1 notation.
                    Examples: "B2:C2", "A1", "Sheet1", "Sheet1!A1:B1", etc..

                "value_input_option" (InputOption, optional): Input option can be:
                    InputOption.USER_ENTERED - All inputs treated as input from 
                    the user (enabling formatting and formulas), or InputOption.RAW - all
                    inputs as is. Defaults to InputOption.USER_ENTERED.

                "dimension" (Dimension, optional): Reading dimension. May be 
                    Dimension.ROWS or Dimension.COLUMNS. Defaults to Dimension.ROWS.

                "table" (List[List[Any]]): Values to add to spreadsheet.

        Raises:
            Exception: If unable to update spreadsheet.

        Returns:
            Dict[str, Any]: Expected keys:
                "spreadsheet" (Dict[str, Any]): Updated spreadsheet;
        """
        try:
            return {
                "spreadsheet": (
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
            }
        except Exception as e:
            raise Exception(f"Unable to update spreadsheet: {e}")


class GoogleSheetsWriteBatch(GoogleSheetsAction[Dict[str, Any], Dict[str, Any]]):
    """
    Write to spreadsheet
    """
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "spreadsheet_id" (str): Spreadsheet ID (can be found
                    in url: https://docs.google.com/spreadsheets/d/***spreadsheet_id***/edit#gid=0);

                "value_input_option" (InputOption, optional): Input option can be:
                    InputOption.USER_ENTERED - All inputs treated as input from 
                    the user (enabling formatting and formulas), or InputOption.RAW - all
                    inputs as is. Defaults to InputOption.USER_ENTERED.
                
                    
                "inputs" (List[Dict[str, Any]]): List of write actions. Each action contain:
                    "cells_range" (str): Range of cells provided in A1 notation.
                        Examples: "B2:C2", "A1", "Sheet1", "Sheet1!A1:B1", etc..

                    "dimension" (Dimension, optional): Reading dimension. May be 
                        Dimension.ROWS or Dimension.COLUMNS. Defaults to Dimension.ROWS.

                    "table" (List[List[Any]]): Values to add to spreadsheet.

        Raises:
            Exception: If unable to update spreadsheet.

        Returns:
            Dict[str, Any]: Expected keys:
                "spreadsheet" (Dict[str, Any]): Updated spreadsheet;
        """
        try:
            return {
                "spreadsheet": (
                    self.sheet_service # type: ignore
                    .values()
                    .batchUpdate(
                        spreadsheetId=input_data["spreadsheet_id"],
                        body={
                            "data": [
                                {
                                    "values": i["table"],
                                    "majorDimension": i.get(
                                        "dimension", Dimension.ROWS
                                    ).value,
                                    "range": i["cells_range"]
                                } for i in input_data["inputs"]
                            ],
                            "valueInputOption": input_data.get(
                                "value_input_option", InputOption.USER_ENTERED
                            ).value,
                        },
                    )
                    .execute()
                )
            }
        except Exception as e:
            raise Exception(f"Unable to update spreadsheet: {e}")


class GoogleSheetsAppend(GoogleSheetsAction[Dict[str, Any], Dict[str, Any]]):
    """
    Append to spreadsheet
    """
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "spreadsheet_id" (str): Spreadsheet ID (can be found
                    in url: https://docs.google.com/spreadsheets/d/***spreadsheet_id***/edit#gid=0);

                "cells_range" (str): Range of cells provided in A1 notation.
                    Examples: "B2:C2", "A1", "Sheet1", "Sheet1!A1:B1", etc..

                "value_input_option" (InputOption, optional): Input option can be:
                    InputOption.USER_ENTERED - All inputs treated as input from 
                    the user (enabling formatting and formulas), or InputOption.RAW - all
                    inputs as is. Defaults to InputOption.USER_ENTERED.

                "insert_data_option" (InsertDataOption, optional): Isert data option can be 
                    InsertDataOption.OVERWRITE - will overwrite anything after table, 
                    or InsertDataOption.INSERT_ROWS - will insert new rows.
                    Defaults to InsertDataOption.OVERWRITE.
                    
                "dimension" (Dimension, optional): Reading dimension. May be 
                    Dimension.ROWS or Dimension.COLUMNS. Defaults to Dimension.ROWS.

                "table" (List[List[Any]]): Values to add to spreadsheet.

        Raises:
            Exception: If unable to update spreadsheet.

        Returns:
            Dict[str, Any]: Expected keys:
                "spreadsheet" (Dict[str, Any]): Updated spreadsheet;
        """
        try:
            return {
                "spreadsheet": (
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
            }
        except Exception as e:
            raise Exception(f"Unable to update spreadsheet: {e}")


class GoogleSheetsCreate(GoogleSheetsAction[Dict[str, Any], Dict[str, Any]]):
    """
    Create spreadsheet
    """
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "title" (str): Name of the spreadsheet;
                
                "sheets" (List[str], optional): Sheets names to create.
                    Defaults to ["Sheet1"].

        Raises:
            Exception: If unable to create spreadsheet.

        Returns:
            Dict[str, Any]: Expected keys:
                "spreadsheet_id" (str): Spreadsheet ID;
        """
        try:
            return {
                "spreadsheet_id": (
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
            }
        except Exception as e:
            raise Exception(f"Unable to create spreadsheet: {e}")