from typing import Type, Dict, Any

from googleapiclient.discovery import build # type: ignore

from core.datasource_level.schema import DatasourceAction
from implementation.datasources.google_cloud.client import GoogleCloudClient
from implementation.datasources.google_docs.schema import GoogleDocsClientConfig, GoogleDocsData

class GoogleDocsClient(GoogleCloudClient[GoogleDocsData]):
    input_class: Type[DatasourceAction] = DatasourceAction
    output_class: Type[GoogleDocsData] = GoogleDocsData

    def __init__(self, cfg: GoogleDocsClientConfig) -> None:
        super().__init__(cfg)
        self.creds = self.authorize(cfg)
        self.service = build("docs", "v1", credentials=self.creds) # type: ignore
        self.docs_service = self.service.documents() # type: ignore


    def invoke(self, input_data: DatasourceAction) -> Dict[str, Any]:
        return input_data.execute(docs_service=self.docs_service) # type: ignore