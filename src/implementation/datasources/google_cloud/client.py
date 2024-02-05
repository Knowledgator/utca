from typing import Optional, cast, Any
import os.path
from abc import ABC

import google.auth # type: ignore
from google.auth.transport.requests import Request # type: ignore
from google.oauth2.credentials import Credentials # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore

from implementation.datasources.google_cloud.schema import (
    GoogleCloudClientConfig
)

class GoogleCloudClient(ABC):
    creds: Optional[Credentials]
    service: Any

    @classmethod
    def authorize(cls, cfg: GoogleCloudClientConfig) -> Credentials:
        creds: Optional[Credentials] = None
        if not cfg.credentials:
            creds, _ = google.auth.default() # type: ignore
            return creds # type: ignore
        
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file( # type: ignore
                "token.json", cfg.scopes
            )
        
        if not creds or not creds.valid or not all(s in cfg.scopes for s in creds.scopes): # type: ignore
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