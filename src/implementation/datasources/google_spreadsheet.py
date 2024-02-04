from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Any, cast, Dict, Union, Generic, TypeVar
from enum import Enum
import os.path

import google.auth # type: ignore
from google.auth.transport.requests import Request # type: ignore
from google.oauth2.credentials import Credentials # type: ignore
from google.auth.compute_engine.credentials import Credentials as CloudCredentials # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from googleapiclient.discovery import build # type: ignore
from googleapiclient.errors import HttpError # type: ignore
from pydantic import BaseModel

# from core.executable_level_1.executable import Executable
# from core.executable_level_1.schema import Input, Output, Config

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1k4pSzvMClric29a_2w-pKjJJQvU2Dq59SrZIy6XUVU4"
SAMPLE_RANGE_NAME = "Аркуш1"

class GoogleSpreadsheetPage(BaseModel):
    table: list[list[Any]]


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


class Action(BaseModel, ABC):
    @abstractmethod
    def execute(self, sheet_service) -> Any: # type: ignore
        ...


class InputOption(Enum):
    RAW = 'RAW'
    USER_ENTERED = 'USER_ENTERED'


class GoogleSpreadsheetRead(Action, Range[GoogleSpreadsheetSelectRange]):
    spreadsheet_id: str
    dimension: Dimension = Dimension.ROWS

    def execute(self, sheet_service) -> GoogleSpreadsheetPage: # type: ignore
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
            return GoogleSpreadsheetPage(table=result.get("values", [])) # type: ignore
        except Exception as e:
            raise ValueError(f'Unable to read specified sheet: {e}')


class GoogleSpreadsheetReadBatch(Action, Ranges[GoogleSpreadsheetSelectRange]):
    spreadsheet_id: str
    dimension: Dimension = Dimension.ROWS

    def execute(self, sheet_service) -> list[GoogleSpreadsheetPage]: # type: ignore
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
            return [GoogleSpreadsheetPage(table=i.get("values", [])) for i in result.get("valueRanges", [])] # type: ignore
        except Exception as e:
            raise ValueError(f'Unable to read specified sheet: {e}')


class GoogleSpreadsheetUpdate(Action, Range[GoogleSpreadsheetWriteRange]):
    spreadsheet_id: str
    value_input_option: InputOption = InputOption.USER_ENTERED

    def execute(self, sheet_service) -> None: # type: ignore
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
        except HttpError as e:
            raise ValueError(f"An error occurred: {e}")


class GoogleSpreadsheetUpdateBatch(Action, Ranges[GoogleSpreadsheetWriteRange]):
    spreadsheet_id: str
    value_input_option: InputOption = InputOption.USER_ENTERED

    def execute(self, sheet_service) -> None: # type: ignore
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
        except HttpError as e:
            raise ValueError(f"An error occurred: {e}")


class InsertDataOption(Enum):
    INSERT_ROWS = 'INSERT_ROWS'
    OVERWRITE = 'OVERWRITE'


class GoogleSpreadsheetAppend(Action, Range[GoogleSpreadsheetWriteRange]):
    spreadsheet_id: str
    value_input_option: InputOption = InputOption.USER_ENTERED
    insert_data_option: InsertDataOption = InsertDataOption.OVERWRITE

    def execute(self, sheet_service) -> None: # type: ignore
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
        except HttpError as e:
            raise ValueError(f"An error occurred: {e}")


class Sheet(BaseModel):
    title: str


class GoogleSpreadsheetCreate(Action):
    spreadsheet_id: str
    title: str

    def execute(self, sheet_service) -> str: # type: ignore
        try:
            return (
                sheet_service # type: ignore
                .create( 
                    body={
                        'properties': {
                            'title': self.title
                        },
                        'sheets': [

                        ]
                    }, 
                    fields='spreadsheetId'
                )
                .execute()
                .get('spreadsheetId')
            )
        except Exception as e:
            raise ValueError(f'Unable to create sheet: {e}')


class GoogleSpreadsheetClientConfig(BaseModel):
    credentials: Union[Dict[str, Any], str]
    scopes: list[str] = [
        "https://www.googleapis.com/auth/spreadsheets"
    ]


class GoogleSpreadsheetClient:
    creds: Union[Credentials, CloudCredentials]

    @classmethod
    def authorize(cls, cfg: GoogleSpreadsheetClientConfig) -> Credentials:
        creds: Optional[Credentials] = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file( # type: ignore
                "token.json", cfg.scopes
            ) 
        
        if not creds or not creds.valid: # type: ignore
            if creds and creds.expired and creds.refresh_token: # type: ignore
                creds.refresh(Request()) # type: ignore
            else:
                flow = InstalledAppFlow.from_client_secrets_file( # type: ignore
                    "credentials.json", cfg.scopes
                ) if isinstance(credentials, str) else InstalledAppFlow.from_client_config( # type: ignore
                    cfg.credentials, cfg.scopes
                )
                creds = flow.run_local_server(port=0) # type: ignore
            
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json()) # type: ignore
        return cast(Credentials, creds)


    def __init__(self, cfg: GoogleSpreadsheetClientConfig) -> None:
        # super().__init__(cfg)
        if cfg.credentials:
            self.creds = self.authorize(cfg)
        else: 
            creds, _ = google.auth.default() # type: ignore
            self.creds = creds # type: ignore
        self.service = build("sheets", "v4", credentials=self.creds) # type: ignore
        self.sheet_service = self.service.spreadsheets() # type: ignore


    def execute(self, action: Action) -> Any:
        return action.execute(self.sheet_service) # type: ignore


if __name__ == "__main__":
    cfg = GoogleSpreadsheetClientConfig(credentials='credentials.json')
    cli = GoogleSpreadsheetClient(cfg)
    read_batch_action = GoogleSpreadsheetReadBatch(
        spreadsheet_id=SAMPLE_SPREADSHEET_ID, 
        select_range=[
            GoogleSpreadsheetSelectRange(page_name='A1:B1'),
            GoogleSpreadsheetSelectRange(page_name='A2:B2')
        ],
        dimension=Dimension.COLUMNS
    )
    # print(GoogleSpreadsheetClient('credentials.json').create('HiThere!'))
    update_action = GoogleSpreadsheetUpdate(
        spreadsheet_id=SAMPLE_SPREADSHEET_ID,
        select_range=GoogleSpreadsheetWriteRange(
            page_name=SAMPLE_RANGE_NAME,
            values=[['A1', 'A2']],
            dimension=Dimension.COLUMNS
        )
    )
    read_action = GoogleSpreadsheetRead(
        spreadsheet_id=SAMPLE_SPREADSHEET_ID,
        dimension=Dimension.ROWS,
        select_range=GoogleSpreadsheetSelectRange(
            page_name=SAMPLE_RANGE_NAME, 
        )
    )
    update_batch_action = GoogleSpreadsheetUpdateBatch(
        spreadsheet_id=SAMPLE_SPREADSHEET_ID,
        select_range=[
            GoogleSpreadsheetWriteRange(
                select_range='A1',
                values=[['Dot']],
            ),
            GoogleSpreadsheetWriteRange(
                select_range='A2:B2',
                values=[['A2', 'B2']],
            )

        ]
    )
    append_action = GoogleSpreadsheetAppend(
        spreadsheet_id=SAMPLE_SPREADSHEET_ID,
        select_range=GoogleSpreadsheetWriteRange(
            page_name=SAMPLE_RANGE_NAME,
            values=[['A1', 'A2'], ['E', 'E']],
            dimension=Dimension.ROWS
        )
    )


    # print(cli.execute(update_action))
    # print(cli.execute(read_batch_action))
    cli.execute(append_action)
    print(cli.execute(read_action))