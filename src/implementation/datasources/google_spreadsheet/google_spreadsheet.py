from __future__ import annotations
from typing import Optional, Any, cast, Union, Dict, Type
import os.path

import google.auth # type: ignore
from google.auth.transport.requests import Request # type: ignore
from google.oauth2.credentials import Credentials # type: ignore
from google.auth.compute_engine.credentials import Credentials as CloudCredentials # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from googleapiclient.discovery import build # type: ignore

from core.datasource_level.datasource import Datasource
from core.datasource_level.schema import DatasourceAction
from implementation.datasources.google_spreadsheet.schema import GoogleSpreadsheetClientConfig, GoogleSpreadsheetData

class GoogleSpreadsheetClient(
    Datasource[GoogleSpreadsheetClientConfig, DatasourceAction, GoogleSpreadsheetData]
):
    input_class: Type[DatasourceAction] = DatasourceAction
    output_class: Type[GoogleSpreadsheetData] = GoogleSpreadsheetData

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
                    cfg.credentials, cfg.scopes
                ) if isinstance(cfg.credentials, str) else InstalledAppFlow.from_client_config( # type: ignore
                    cfg.credentials, cfg.scopes
                )
                creds = flow.run_local_server(port=0) # type: ignore
            
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json()) # type: ignore
        return cast(Credentials, creds)


    def __init__(self, cfg: GoogleSpreadsheetClientConfig) -> None:
        super().__init__(cfg)
        if cfg.credentials:
            self.creds = self.authorize(cfg)
        else: 
            creds, _ = google.auth.default() # type: ignore
            self.creds = creds # type: ignore
        self.service = build("sheets", "v4", credentials=self.creds) # type: ignore
        self.sheet_service = self.service.spreadsheets() # type: ignore


    def invoke(self, input_data: DatasourceAction) -> Dict[str, Any]:
        return input_data.execute(sheet_service=self.sheet_service) # type: ignore