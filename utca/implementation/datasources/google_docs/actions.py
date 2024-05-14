from typing import Any, Dict, Optional

from utca.core.executable_level_1.actions import (
    Action, ActionInput, ActionOutput
)
from utca.implementation.apis.google_cloud.client import (
    GoogleCloudClient
)

# TODO: docs templating (casual update but with copying file and update copy)
# updates = [
#         {
#         "replaceAllText": {
#             "containsText": {
#                 "text": "{{customer-name}}", # placeholder
#                 "matchCase":  "true"
#             },
#             "replaceText": customer_name,
#         }}, {
#         "replaceAllText": {
#             "containsText": {
#                 "text": "{{date}}",
#                 "matchCase":  "true"
#             },
#             "replaceText": str(date),
#         }
#     }
# ]

class GoogleDocsAction(Action[ActionInput, ActionOutput]):
    """
    Base Google Documents action
    """
    def __init__(
        self, 
        client: GoogleCloudClient,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            client (GoogleCloudClient): Google client that will be used for access.

            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.docs_service = client.service.documents()


class GoogleDocsCreate(GoogleDocsAction[Dict[str, Any], Dict[str, Any]]):
    """
    Create document
    """
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "title" (str): Name of the document;

        Raises:
            Exception: If unable to create document.

        Returns:
            Dict[str, Any]: Expected keys:
                "document_id" (str): Document ID;
        """
        try:
            doc_id: str = ( # type: ignore
                self.docs_service # type: ignore
                .create(
                    body={
                        "title": input_data["title"]
                    },
                    fields="documentId"
                )
                .execute()
            )
            return {"document_id": doc_id}
        except Exception as e:
            raise Exception(f"Unable to create document: {e}")


class GoogleDocsWrite(GoogleDocsAction[Dict[str, Any], Dict[str, Any]]):
    """
    Write to document
    """
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "document_id" (str): ID of the document. Document ID (can be found
                    in url: https://docs.google.com/documents/d/***document_id***/edit#gid=0);

                "requests" (Dict[str, Any]): Actions for updating the document.

        Raises:
            Exception: If unable to update document.

        Returns:
            Dict[str, Any]: Expected keys:
                "document" (Dict[str, Any]): Updated document;
        """
        try:
            return {
                "document": (
                    self.docs_service # type: ignore
                    .batchUpdate(
                        documentId=input_data["document_id"], 
                        body={"requests": input_data["requests"]}
                    ).execute()
                )
            }
        except Exception as e:
            raise Exception(f"Unable to update document: {e}")


class GoogleDocsRead(GoogleDocsAction[Dict[str, Any], Dict[str, Any]]):
    """
    Read document
    """
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "document_id" (str): ID of the document. Document ID (can be found
                    in url: https://docs.google.com/documents/d/***document_id***/edit#gid=0);

        Raises:
            Exception: If unable to read document.

        Returns:
            Dict[str, Any]: Expected keys:
                "document" (Dict[str, Any]): Document;
        """
        try:
            return {
                "document": (
                    self.docs_service # type: ignore
                    .get(
                        documentId=input_data["document_id"]
                    ).execute()
                )
            }
        except Exception as e:
            raise ValueError(f"Unable to read document: {e}")