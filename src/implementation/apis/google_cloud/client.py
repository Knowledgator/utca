from typing import Optional, cast, Any, Union, Dict
import os.path

import google.auth # type: ignore
from google.auth.transport.requests import Request # type: ignore
from google.oauth2.credentials import Credentials # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from googleapiclient.discovery import build # type: ignore

from implementation.apis.google_cloud.schema import (
    GoogleCloudClientConfig
)

class GoogleCloudClient: # TODO: issue with missmatched scopes
    creds: Optional[Credentials]
    service: Any

    @classmethod
    def authorize(
        cls, 
        scopes: list[str],
        credentials: Union[Dict[str, Any], str, None]=None,
    ) -> Credentials:
        creds: Optional[Credentials] = None
        if not credentials:
            creds, _ = google.auth.default() # type: ignore
            return creds # type: ignore
        
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file( # type: ignore
                "token.json", scopes
            )

        if not creds or not creds.valid or not all(s in cfg.scopes for s in creds.scopes): # type: ignore
            if creds and creds.expired and creds.refresh_token: # type: ignore
                creds.refresh(Request()) # type: ignore
            else:
                flow = (
                    InstalledAppFlow.from_client_secrets_file( # type: ignore
                        credentials, scopes
                    ) if isinstance(credentials, str) else 
                    InstalledAppFlow.from_client_config( # type: ignore
                        credentials, scopes
                    )
                )
                creds = flow.run_local_server(port=0) # type: ignore
            
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json()) # type: ignore
        return cast(Credentials, creds)
    

    def __init__(self, cfg: GoogleCloudClientConfig) -> None:
        self.creds = self.authorize(cfg.scopes, cfg.credentials)
        self.service = build(
            cfg.service, 
            cfg.version,
            credentials=self.creds
        )