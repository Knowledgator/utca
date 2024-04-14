from typing import (
    Any, Dict, List, Optional, Union, cast
) 
import os.path
import os

import google.auth # type: ignore
from google.auth.transport.requests import Request # type: ignore
from google.oauth2.credentials import Credentials # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from googleapiclient.discovery import build # type: ignore

from core.constants import DEFAULT_TOKENS_DIRECTORY
from implementation.apis.google_cloud.schema import (
    GoogleCloudClientConfig
)

class GoogleCloudClient:
    creds: Optional[Credentials]
    service: Any

    @classmethod
    def verify_creds(
        cls, 
        scopes: List[str],
        credentials: Optional[Union[Dict[str, Any], str]]=None,
    ) -> Credentials:
        flow = (
            InstalledAppFlow.from_client_secrets_file( # type: ignore
                credentials, scopes
            ) if isinstance(credentials, str) else 
            InstalledAppFlow.from_client_config( # type: ignore
                credentials, scopes
            )
        )
        return flow.run_local_server(port=0) # type: ignore


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
        
        src = (
            os.getenv('UTCA_TOKENS_DIRECTORY', DEFAULT_TOKENS_DIRECTORY)
            + f"/google/token.json"
        )
        if os.path.exists(src):
            creds = Credentials.from_authorized_user_file( # type: ignore
                src, scopes
            )

        if not creds:
            creds = cls.verify_creds(scopes, credentials)
        elif not all(s in scopes for s in creds.scopes): # type: ignore
            scopes = cast(List[str], [*creds.scopes, *scopes]) # type: ignore
            creds = cls.verify_creds(scopes, credentials)
        elif not creds.valid:
            try:
                creds.refresh(Request()) # type: ignore
            except Exception:
                creds = cls.verify_creds(scopes, credentials) # type: ignore
            
        # Save the credentials for the next run
        with open(src, "w") as token:
            token.write(creds.to_json()) # type: ignore
        return creds
    

    def __init__(self, cfg: GoogleCloudClientConfig) -> None:
        self.creds = self.authorize(cfg.scopes, cfg.credentials)
        self.service = build(
            cfg.service, 
            cfg.version,
            credentials=self.creds
        )