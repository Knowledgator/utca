from typing import Optional

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


    def read(
        self, 
        cfg: Optional[GoogleSpreadsheetReadConfig] = None
    ) -> GoogleSpreadsheetRead:
        cfg = cfg or GoogleSpreadsheetReadConfig()
        cfg.set_service(self.sheet_service) # type: ignore
        return GoogleSpreadsheetRead(cfg)


    def write(
        self, 
        cfg: Optional[GoogleSpreadsheetWriteConfig] = None
    ) -> GoogleSpreadsheetWrite:
        cfg = cfg or GoogleSpreadsheetWriteConfig()
        cfg.set_service(self.sheet_service) # type: ignore
        return GoogleSpreadsheetWrite(cfg)
    

    def append(
        self, 
        cfg: Optional[GoogleSpreadsheetAppendConfig] = None
    ) -> GoogleSpreadsheetAppend:
        cfg = cfg or GoogleSpreadsheetAppendConfig()
        cfg.set_service(self.sheet_service) # type: ignore
        return GoogleSpreadsheetAppend(cfg)


    def create(
        self, 
        cfg: Optional[GoogleSpreadsheetCreateConfig] = None
    ) -> GoogleSpreadsheetCreate:
        cfg = cfg or GoogleSpreadsheetCreateConfig()
        cfg.set_service(self.sheet_service) # type: ignore
        return GoogleSpreadsheetCreate(cfg)