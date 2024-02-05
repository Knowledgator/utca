from typing import Any, Dict

from core.datasource_level.schema import DatasourceAction

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

class GoogleDocsCreate(DatasourceAction):
    title: str

    def execute(self, docs_service) -> Dict[str, Any]: # type: ignore
        try:
            (
                docs_service # type: ignore
                .create(
                    body={
                        'title': self.title
                    }
                )
                .execute()
            )
            return {}
        except Exception as e:
            raise ValueError(f'Unable to create doc: {e}')
        

class GoogleDocsUpdate(DatasourceAction):
    document_id: str
    updates: list[Dict[str, Any]]

    def execute(self, docs_service) -> Dict[str, Any]: # type: ignore
        try:
            (
                docs_service # type: ignore
                .batchUpdate(
                    documentId=self.document_id, 
                    body={'requests': self.updates}
                ).execute()
            )
            return {}
        except Exception as e:
            raise ValueError(f'Unable to update doc: {e}')


class GoogleDocsRead(DatasourceAction):
    document_id: str

    def execute(self, docs_service) -> Dict[str, Any]: # type: ignore
        try:
            return (
                docs_service # type: ignore
                .get(
                    documentId=self.document_id
                ).execute()
            )
        except Exception as e:
            raise ValueError(f'Unable to read doc: {e}')