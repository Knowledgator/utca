from typing import Any, Dict, Type

from core.datasource_level_2.datasource import DatasourceAction
from implementation.datasources.google_docs.schema import (
    GoogleDocsReadConfig,
    GoogleDocsReadInput,
    GoogleDocsReadOutput,
    GoogleDocsWriteConfig,
    GoogleDocsWriteInput,
    GoogleDocsWriteOutput,
    GoogleDocsCreateConfig,
    GoogleDocsCreateInput,
    GoogleDocsCreateOutput
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

class GoogleDocsCreate(
    DatasourceAction[
        GoogleDocsCreateConfig,
        GoogleDocsCreateInput,
        GoogleDocsCreateOutput
    ]
):
    input_class: Type[GoogleDocsCreateInput] = GoogleDocsCreateInput
    output_class: Type[GoogleDocsCreateOutput] = GoogleDocsCreateOutput
    
    def invoke(self, input_data: GoogleDocsCreateInput) -> Dict[str, Any]: # type: ignore
        try:
            doc_id: str = ( # type: ignore
                docs_service # type: ignore
                .create(
                    body={
                        'title': input_data.title
                    },
                    fields='spreadsheetId'
                )
                .execute()
            )
            return {'doc_id': doc_id}
        except Exception as e:
            raise ValueError(f'Unable to create doc: {e}')
        
    
    def invoke_batch(self, input_data: list[GoogleDocsCreateInput]) -> list[Dict[str, Any]]:
        raise Exception('Not implemented')
        

class GoogleDocsWrite(
    DatasourceAction[
        GoogleDocsWriteConfig,
        GoogleDocsWriteInput,
        GoogleDocsWriteOutput,
    ]
):
    input_class: Type[GoogleDocsWriteInput] = GoogleDocsWriteInput
    output_class: Type[GoogleDocsWriteOutput] = GoogleDocsWriteOutput

    def invoke(self, input_data: GoogleDocsWriteInput) -> Dict[str, Any]: # type: ignore
        try:
            (
                self.cfg.service # type: ignore
                .batchUpdate(
                    documentId=self.cfg.document_id, 
                    body={'requests': [input_data.action]}
                ).execute()
            )
            return {}
        except Exception as e:
            raise ValueError(f'Unable to update doc: {e}')


    def invoke_batch(self, input_data: list[GoogleDocsWriteInput]) -> list[Dict[str, Any]]:
        try:
            (
                self.cfg.service # type: ignore
                .batchUpdate(
                    documentId=self.cfg.document_id, 
                    body={'requests': [i.action for i in input_data]}
                ).execute()
            )
            return []
        except Exception as e:
            raise ValueError(f'Unable to update doc: {e}')


class GoogleDocsRead(
    DatasourceAction[
        GoogleDocsReadConfig,
        GoogleDocsReadInput,
        GoogleDocsReadOutput,
    ]
):
    input_class: Type[GoogleDocsReadInput] = GoogleDocsReadInput
    output_class: Type[GoogleDocsReadOutput] = GoogleDocsReadOutput

    def invoke(self, input_data: GoogleDocsReadInput) -> Dict[str, Any]:
        try:
            return (
                self.cfg.service # type: ignore
                .get(
                    documentId=input_data.document_id
                ).execute()
            )
        except Exception as e:
            raise ValueError(f'Unable to read doc: {e}')
        
    
    def invoke_batch(self, input_data: list[GoogleDocsReadInput]) -> list[Dict[str, Any]]:
        raise Exception('Not implemented')