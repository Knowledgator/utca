from typing import Any, Dict

from core.executable_level_1.actions import (
    Action, OneToOne, InputState, OutputState
)
from implementation.apis.google_cloud.client import (
    GoogleCloudClient
)

# TODO: docs templating (casual update but with copying file and update copy)
# updates = [
#         {
#         'replaceAllText': {
#             'containsText': {
#                 'text': '{{customer-name}}', # placeholder
#                 'matchCase':  'true'
#             },
#             'replaceText': customer_name,
#         }}, {
#         'replaceAllText': {
#             'containsText': {
#                 'text': '{{date}}',
#                 'matchCase':  'true'
#             },
#             'replaceText': str(date),
#         }
#     }
# ]

class GoogleDocsAction(Action[InputState, OutputState]):
    def __init__(self, client: GoogleCloudClient) -> None:
        self.docs_service = client.service.documents()


@OneToOne
class GoogleDocsCreate(GoogleDocsAction[Dict[str, Any], Dict[str, Any]]):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            doc_id: str = ( # type: ignore
                self.docs_service # type: ignore
                .create(
                    body={
                        'title': input_data["title"]
                    },
                    fields='documentId'
                )
                .execute()
            )
            return {'doc_id': doc_id}
        except Exception as e:
            raise ValueError(f'Unable to create doc: {e}')


@OneToOne
class GoogleDocsWrite(GoogleDocsAction[Dict[str, Any], Dict[str, Any]]):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            input_data["document"] = (
                self.docs_service # type: ignore
                .batchUpdate(
                    documentId=input_data["document_id"], 
                    body={'requests': input_data["actions"]}
                ).execute()
            )
            return input_data
        except Exception as e:
            raise ValueError(f'Unable to update doc: {e}')


@OneToOne
class GoogleDocsRead(GoogleDocsAction[Dict[str, Any], Dict[str, Any]]):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            return (
                self.docs_service # type: ignore
                .get(
                    documentId=input_data["document_id"]
                ).execute()
            )
        except Exception as e:
            raise ValueError(f'Unable to read doc: {e}')