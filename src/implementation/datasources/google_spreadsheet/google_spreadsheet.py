from __future__ import annotations

from googleapiclient.discovery import build # type: ignore

from implementation.datasources.google_cloud.client import (
    GoogleCloudClient
)
from implementation.datasources.google_spreadsheet.schema import (
    GoogleSpreadsheetClientConfig,
    GoogleSpreadsheetReadConfig,
    GoogleSpreadsheetWriteConfig,
    GoogleSpreadsheetAppendConfig,
    GoogleSpreadsheetCreateConfig,
)
from implementation.datasources.google_spreadsheet.actions import (
    GoogleSpreadsheetRead,
    GoogleSpreadsheetWrite,
    GoogleSpreadsheetAppend,
    GoogleSpreadsheetCreate
)

class GoogleSpreadsheetClient(GoogleCloudClient):
    def __init__(self, cfg: GoogleSpreadsheetClientConfig) -> None:
        self.creds = self.authorize(cfg)
        self.service = build("sheets", "v4", credentials=self.creds) # type: ignore
        self.sheet_service = self.service.spreadsheets() # type: ignore


    def read(self, read_config: GoogleSpreadsheetReadConfig) -> GoogleSpreadsheetRead:
        read_config.set_service(self.sheet_service) # type: ignore
        return GoogleSpreadsheetRead(read_config)


    def write(self, write_config: GoogleSpreadsheetWriteConfig) -> GoogleSpreadsheetWrite:
        write_config.set_service(self.sheet_service) # type: ignore
        return GoogleSpreadsheetWrite(write_config)
    

    def append(self, append_config: GoogleSpreadsheetAppendConfig) -> GoogleSpreadsheetAppend:
        append_config.set_service(self.sheet_service) # type: ignore
        return GoogleSpreadsheetAppend(append_config)


    def create(self, create_config: GoogleSpreadsheetCreateConfig) -> GoogleSpreadsheetCreate:
        create_config.set_service(self.sheet_service) # type: ignore
        return GoogleSpreadsheetCreate(create_config)