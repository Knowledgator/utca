import logging

from implementation.apis.google_cloud.client import GoogleCloudClient
from implementation.datasources.google_docs.schema import (
    GoogleDocsClientConfig
)
from implementation.datasources.google_docs.actions import (
    GoogleDocsRead,
    GoogleDocsWrite
)

def test_docs():
    # The ID of a sample document.
    DOCUMENT_ID = "1qDrWeHqblOOakVCIc7FJUr8u2rAhRdj2YSb4SgTz96g"
    client = GoogleCloudClient(
        GoogleDocsClientConfig(
            credentials="src/implementation/datasources/google_docs/__test__/credentials.json"
        )
    )

    # template_action = GoogleDocsUpdate(
    #     document_id=DOCUMENT_ID,
    #     updates=[{
    #         "replaceAllText": {
    #             "containsText": {
    #                 "text": "{{template_placeholder}}", # placeholder
    #                 "matchCase":  "true"
    #             },
    #             "replaceText": "HEY!!!!!!!!!!!!",
    #         }
    #     }]
    # )
    # delete_action = GoogleDocsUpdate(
    #     document_id=DOCUMENT_ID,
    #     updates=[{
    #         "deleteContentRange": {
    #             "range": {
    #                 "startIndex": 18,
    #                 "endIndex": 50,
    #             }

    #         }

    #     }]
    # )

    GoogleDocsWrite(client).execute({
            "document_id": DOCUMENT_ID,
            "actions": [{
                "insertText": {
                    "location": {
                        "index": 19,
                    },
                    "text": "{{template_placeholder}}\n" # "\n" is mandatory for new paragraph
                },
            }]
    })
    logging.error(
        GoogleDocsRead(client).execute({"document_id": DOCUMENT_ID})
    )


# a = [
#     {
#         "endIndex": 1, 
#         "sectionBreak": {
#             "sectionStyle": {
#                 "columnSeparatorStyle": "NONE", 
#                 "contentDirection": "LEFT_TO_RIGHT", 
#                 "sectionType": "CONTINUOUS"
#             }
#         }
#     }, 
#     {
#         "startIndex": 1, 
#         "endIndex": 19, 
#         "paragraph": {
#             "elements": [
#                 {
#                     "startIndex": 1, 
#                     "endIndex": 19, 
#                     "textRun": {
#                         "content": "SOME TEXT I GUESS\n", 
#                         "textStyle": {}
#                     }
#                 }
#             ], 
#             "paragraphStyle": {
#                 "namedStyleType": "NORMAL_TEXT", 
#                 "direction": "LEFT_TO_RIGHT"
#             }
#         }
#     }, 
#     {
#         "startIndex": 19, 
#         "endIndex": 20, 
#         "paragraph": {
#             "elements": [
#                 {
#                     "startIndex": 19, 
#                     "endIndex": 20, 
#                     "textRun": {
#                         "content": "\n", 
#                         "textStyle": {}
#                     }
#                 }
#             ], 
#             "paragraphStyle": {
#                 "namedStyleType": "NORMAL_TEXT",
#                 "direction": "LEFT_TO_RIGHT"
#             }
#         }
#     }, 
#     {
#         "startIndex": 20, 
#         "endIndex": 31, 
#         "paragraph": {
#             "elements": [
#                 {
#                     "startIndex": 20, 
#                     "endIndex": 31, 
#                     "textRun": {
#                         "content": "LARGE COCK\n", 
#                         "textStyle": {}
#                     }
#                 }
#             ], 
#             "paragraphStyle": {
#                 "namedStyleType": "NORMAL_TEXT", 
#                 "direction": "LEFT_TO_RIGHT"
#             }
#         }
#     }
# ]