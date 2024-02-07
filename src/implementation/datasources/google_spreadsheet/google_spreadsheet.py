from __future__ import annotations

from googleapiclient.discovery import build # type: ignore

from core.datasource_level_2.datasource import DatasourceManager
from implementation.apis.google_cloud.client import (
    GoogleCloudClient
)
from implementation.datasources.google_spreadsheet.schema import (
    GoogleSpreadsheetClientConfig,
    GoogleSpreadsheetReadConfig,
    GoogleSpreadsheetReadInput,
    GoogleSpreadsheetReadOutput,
    GoogleSpreadsheetWriteConfig,
    GoogleSpreadsheetWriteInput,
    GoogleSpreadsheetWriteOutput,
    GoogleSpreadsheetAppendConfig,
    GoogleSpreadsheetCreateConfig,
)
from implementation.datasources.google_spreadsheet.actions import (
    GoogleSpreadsheetRead,
    GoogleSpreadsheetWrite,
    GoogleSpreadsheetAppend,
    GoogleSpreadsheetCreate
)

class GoogleSpreadsheetClient(
    DatasourceManager[
        GoogleSpreadsheetReadConfig,
        GoogleSpreadsheetReadInput,
        GoogleSpreadsheetReadOutput,
        GoogleSpreadsheetWriteConfig,
        GoogleSpreadsheetWriteInput,
        GoogleSpreadsheetWriteOutput
    ], 
    GoogleCloudClient
):
    def __init__(self, cfg: GoogleSpreadsheetClientConfig) -> None:
        self.creds = self.authorize(cfg)
        self.service = build("sheets", "v4", credentials=self.creds) # type: ignore
        self.sheet_service = self.service.spreadsheets() # type: ignore


    def read(self, cfg: GoogleSpreadsheetReadConfig) -> GoogleSpreadsheetRead:
        cfg.set_service(self.sheet_service) # type: ignore
        return GoogleSpreadsheetRead(cfg)


    def write(self, cfg: GoogleSpreadsheetWriteConfig) -> GoogleSpreadsheetWrite:
        cfg.set_service(self.sheet_service) # type: ignore
        return GoogleSpreadsheetWrite(cfg)
    

    def append(self, cfg: GoogleSpreadsheetAppendConfig) -> GoogleSpreadsheetAppend:
        cfg.set_service(self.sheet_service) # type: ignore
        return GoogleSpreadsheetAppend(cfg)


    def create(self, cfg: GoogleSpreadsheetCreateConfig) -> GoogleSpreadsheetCreate:
        cfg.set_service(self.sheet_service) # type: ignore
        return GoogleSpreadsheetCreate(cfg)