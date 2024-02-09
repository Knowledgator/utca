from typing import Optional

from googleapiclient.discovery import build # type: ignore

from core.datasource_level_2.datasource import DatasourceManager
from implementation.apis.google_cloud.client import (
    GoogleCloudClient
)
from implementation.datasources.google_docs.actions import (
    GoogleDocsCreate,
    GoogleDocsRead,
    GoogleDocsWrite
)
from implementation.datasources.google_docs.schema import (
    GoogleDocsClientConfig,
    GoogleDocsReadConfig,
    GoogleDocsReadInput,
    GoogleDocsReadOutput,
    GoogleDocsWriteConfig,
    GoogleDocsWriteInput,
    GoogleDocsWriteOutput,
    GoogleDocsCreateConfig
)

class GoogleDocsClient(
    DatasourceManager[
        GoogleDocsReadConfig,
        GoogleDocsReadInput,
        GoogleDocsReadOutput,
        GoogleDocsWriteConfig,
        GoogleDocsWriteInput,
        GoogleDocsWriteOutput,
    ], 
    GoogleCloudClient
):
    def __init__(self, cfg: GoogleDocsClientConfig) -> None:
        self.creds = self.authorize(cfg)
        self.service = build("docs", "v1", credentials=self.creds) # type: ignore
        self.docs_service = self.service.documents() # type: ignore


    def read(
        self, 
        cfg: Optional[GoogleDocsReadConfig]=None
    ) -> GoogleDocsRead:
        cfg = cfg or GoogleDocsReadConfig()
        cfg.set_service(self.docs_service) # type: ignore
        return GoogleDocsRead(cfg)


    def write(
        self, 
        cfg: Optional[GoogleDocsWriteConfig]=None
    ) -> GoogleDocsWrite:
        cfg = cfg or GoogleDocsWriteConfig()
        cfg.set_service(self.docs_service) # type: ignore
        return GoogleDocsWrite(cfg)


    def create(
        self, 
        cfg: Optional[GoogleDocsCreateConfig]=None
    ) -> GoogleDocsCreate:
        cfg = cfg or GoogleDocsCreateConfig()
        cfg.set_service(self.docs_service) # type: ignore
        return GoogleDocsCreate(cfg)