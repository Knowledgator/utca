import logging

from implementation.datasources.google_docs.google_docs import GoogleDocsClient
from implementation.datasources.google_docs.schema import (
    GoogleDocsClientConfig,
    GoogleDocsWriteInput,
    GoogleDocsReadConfig,
    GoogleDocsReadInput

)

def test_docs():
    # The ID of a sample document.
    DOCUMENT_ID = "1qDrWeHqblOOakVCIc7FJUr8u2rAhRdj2YSb4SgTz96g"
    cli = GoogleDocsClient(GoogleDocsClientConfig(credentials='__test__/credentials.json'))

    # template_action = GoogleDocsUpdate(
    #     document_id=DOCUMENT_ID,
    #     updates=[{
    #         'replaceAllText': {
    #             'containsText': {
    #                 'text': '{{template_placeholder}}', # placeholder
    #                 'matchCase':  'true'
    #             },
    #             'replaceText': 'HEY!!!!!!!!!!!!',
    #         }
    #     }]
    # )
    # delete_action = GoogleDocsUpdate(
    #     document_id=DOCUMENT_ID,
    #     updates=[{
    #         'deleteContentRange': {
    #             'range': {
    #                 'startIndex': 18,
    #                 'endIndex': 50,
    #             }

    #         }

    #     }]
    # )

    cli.write().execute(
        GoogleDocsWriteInput(
            document_id=DOCUMENT_ID,
            action={
                'insertText': {
                    'location': {
                        'index': 19,
                    },
                    'text': '{{template_placeholder}}\n' # '\n' is mandatory for new paragraph
                },

            }
        )
    )
    logging.error(
        cli.read(GoogleDocsReadConfig())
        .execute(GoogleDocsReadInput(document_id=DOCUMENT_ID))
    )


# a = [
#     {
#         'endIndex': 1, 
#         'sectionBreak': {
#             'sectionStyle': {
#                 'columnSeparatorStyle': 'NONE', 
#                 'contentDirection': 'LEFT_TO_RIGHT', 
#                 'sectionType': 'CONTINUOUS'
#             }
#         }
#     }, 
#     {
#         'startIndex': 1, 
#         'endIndex': 19, 
#         'paragraph': {
#             'elements': [
#                 {
#                     'startIndex': 1, 
#                     'endIndex': 19, 
#                     'textRun': {
#                         'content': 'SOME TEXT I GUESS\n', 
#                         'textStyle': {}
#                     }
#                 }
#             ], 
#             'paragraphStyle': {
#                 'namedStyleType': 'NORMAL_TEXT', 
#                 'direction': 'LEFT_TO_RIGHT'
#             }
#         }
#     }, 
#     {
#         'startIndex': 19, 
#         'endIndex': 20, 
#         'paragraph': {
#             'elements': [
#                 {
#                     'startIndex': 19, 
#                     'endIndex': 20, 
#                     'textRun': {
#                         'content': '\n', 
#                         'textStyle': {}
#                     }
#                 }
#             ], 
#             'paragraphStyle': {
#                 'namedStyleType': 'NORMAL_TEXT',
#                 'direction': 'LEFT_TO_RIGHT'
#             }
#         }
#     }, 
#     {
#         'startIndex': 20, 
#         'endIndex': 31, 
#         'paragraph': {
#             'elements': [
#                 {
#                     'startIndex': 20, 
#                     'endIndex': 31, 
#                     'textRun': {
#                         'content': 'LARGE COCK\n', 
#                         'textStyle': {}
#                     }
#                 }
#             ], 
#             'paragraphStyle': {
#                 'namedStyleType': 'NORMAL_TEXT', 
#                 'direction': 'LEFT_TO_RIGHT'
#             }
#         }
#     }
# ]