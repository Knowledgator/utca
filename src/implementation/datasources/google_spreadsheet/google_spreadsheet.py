from __future__ import annotations
from typing import Any, Dict, Type

from googleapiclient.discovery import build # type: ignore

from core.datasource_level.schema import DatasourceAction
from implementation.datasources.google_cloud.client import GoogleCloudClient
from implementation.datasources.google_spreadsheet.schema import GoogleSpreadsheetClientConfig, GoogleSpreadsheetData

class GoogleSpreadsheetClient(GoogleCloudClient[GoogleSpreadsheetData]):
    input_class: Type[DatasourceAction] = DatasourceAction
    output_class: Type[GoogleSpreadsheetData] = GoogleSpreadsheetData


    def __init__(self, cfg: GoogleSpreadsheetClientConfig) -> None:
        super().__init__(cfg)
        self.creds = self.authorize(cfg)
        self.service = build("sheets", "v4", credentials=self.creds) # type: ignore
        self.sheet_service = self.service.spreadsheets() # type: ignore


    def invoke(self, input_data: DatasourceAction) -> Dict[str, Any]:
        return input_data.execute(sheet_service=self.sheet_service) # type: ignore