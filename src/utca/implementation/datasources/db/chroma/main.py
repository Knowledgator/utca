from typing import Any, Dict, Optional, cast

from chromadb import Collection, EmbeddingFunction
from chromadb.api import ClientAPI
from chromadb.api.types import Embeddable, QueryResult, GetResult
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

from utca.core.executable_level_1.actions import Action, ActionInput, ActionOutput

class ChromaDBAction(Action[ActionInput, ActionOutput]):
    def __init__(
        self, 
        client: ClientAPI,
        name: Optional[str]=None,
        default_key: str="output",
    ) -> None:
        """
        Args:
            client (ClientAPI): ChromaDB client to use

            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.

            default_key (str, optional): Default key used for results that is not of type Dict.
                Defaults to "output".
        """
        super().__init__(name, default_key=default_key)
        self.client = client


class ChromaDBRetrieveCollectionAction(ChromaDBAction[str, Collection]):
    def __init__(
        self, 
        client: ClientAPI,
        embedding_function: Optional[EmbeddingFunction[Embeddable]]=None,
        metadata: Optional[Dict[str, Any]] = None,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            client (ClientAPI): ChromaDB client to use

            embedding_function (Optional[EmbeddingFunction[Embeddable]], optional): Embedding function to use.
                If equals to None, default will be used. Defaults to None.

            metadata (Optional[Dict[str, Any]], optional): Collection metadata. Defaults to None.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(client, name, "collection")
        self.embedding_function = cast(
            EmbeddingFunction[Embeddable], embedding_function or DefaultEmbeddingFunction()
        )
        self.metadata = metadata


class ChromaDBCreateCollection(ChromaDBRetrieveCollectionAction):
    """
    Create collection

    Args:
        input_data (str): The name of the collection to create.
    Returns:
        Collection: The newly created collection.
    """
    def execute(self, input_data: str) -> Collection:
        """
        Args:
            input_data (str): The name of the collection to create.
        Returns:
            Collection: The newly created collection.
        """
        return self.client.create_collection(
            name=input_data, 
            metadata=self.metadata,
            embedding_function=self.embedding_function,
        )
    

class ChromaDBGetCollection(ChromaDBRetrieveCollectionAction):
    """
    Get collection

    Args:
        input_data: The name of the collection to get.
    Returns:
        Collection: Retrieved collection.
    """
    def execute(self, input_data: str) -> Collection:
        """
        Args:
            input_data: The name of the collection to get.
        Returns:
            Collection: Retrieved collection.
        """
        return self.client.get_collection(
            name=input_data, 
            embedding_function=self.embedding_function
        )
    

class ChromaDBGetOrCreateCollection(ChromaDBRetrieveCollectionAction):
    """
    Get or Create collection
    """
    def execute(self, input_data: str) -> Collection:
        """
        Args:
            input_data: The name of the collection to get or create.
        Returns:
            Collection: Retrieved collection.
        """
        return self.client.get_or_create_collection(
            name=input_data, 
            embedding_function=self.embedding_function
        )
    

class ChromaDBDeleteCollection(ChromaDBAction[str, None]):
    """
    Delete collection

    Args:
        input_data (str): The name of the collection to delete.
    """
    def execute(self, input_data: str) -> None:
        """
        Args:
            input_data (str): The name of the collection to delete.
        """
        self.client.delete_collection(
            name=input_data
        )


class ChromaDBCollectionAdd(Action[Dict[str, Any], None]):
    """
    Add embeddings to the data store.
    
    Args:
        input_data (Dict[str, Any]): Expected keys:
            "collection" (Collection): Collection to use.
            
            "ids": The ids of the embeddings you wish to add.

            "embeddings": The embeddings to add. If None, embeddings will be computed based on the documents or images using the embedding_function set for the Collection. Optional.
            
            "metadatas": The metadata to associate with the embeddings. When querying, you can filter on this metadata. Optional.
            
            "documents": The documents to associate with the embeddings. Optional.
            
            "images": The images to associate with the embeddings. Optional.
            
            "uris": The uris of the images to associate with the embeddings. Optional.
    """
    def execute(self, input_data: Dict[str, Any]) -> None:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "collection" (Collection): Collection to use.
                
                "ids": The ids of the embeddings you wish to add.

                "embeddings": The embeddings to add. If None, embeddings will be computed based on the documents or images using the embedding_function set for the Collection. Optional.
                
                "metadatas": The metadata to associate with the embeddings. When querying, you can filter on this metadata. Optional.
                
                "documents": The documents to associate with the embeddings. Optional.
                
                "images": The images to associate with the embeddings. Optional.
                
                "uris": The uris of the images to associate with the embeddings. Optional.
        """
        collection: Collection = input_data["collection"]
        collection.add( # type: ignore
            ids=input_data["ids"],
            embeddings=input_data.get("embeddings"),
            metadatas=input_data.get("metadatas"),
            documents=input_data.get("documents"),
            images=input_data.get("images"),
            uris=input_data.get("uris"),
        )


class ChromaDBCollectionUpdate(Action[Dict[str, Any], None]):
    """
    Update the embeddings, metadatas or documents for provided ids.
    
    Args:
        input_data (Dict[str, Any]): Expected keys:
            "collection" (Collection): Collection to use.
            
            "ids": The ids of the embeddings to update.

            "embeddings": The embeddings to update. If None, embeddings will be computed based on the documents or images using the embedding_function set for the Collection. Optional.
            
            "metadatas": The metadata to associate with the embeddings. When querying, you can filter on this metadata. Optional.
            
            "documents": The documents to associate with the embeddings. Optional.
            
            "images": The images to associate with the embeddings. Optional.
            
            "uris": The uris of the images to associate with the embeddings. Optional.
    """
    def execute(self, input_data: Dict[str, Any]) -> None:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "collection" (Collection): Collection to use.
                
                "ids": The ids of the embeddings to update.

                "embeddings": The embeddings to update. If None, embeddings will be computed based on the documents or images using the embedding_function set for the Collection. Optional.
                
                "metadatas": The metadata to associate with the embeddings. When querying, you can filter on this metadata. Optional.
                
                "documents": The documents to associate with the embeddings. Optional.
                
                "images": The images to associate with the embeddings. Optional.
                
                "uris": The uris of the images to associate with the embeddings. Optional.
        """
        collection: Collection = input_data["collection"]
        collection.update( # type: ignore
            ids=input_data["ids"],
            embeddings=input_data.get("embeddings"),
            metadatas=input_data.get("metadatas"),
            documents=input_data.get("documents"),
            images=input_data.get("images"),
            uris=input_data.get("uris"),
        )


class ChromaDBCollectionUpsert(Action[Dict[str, Any], None]):
    """
    Update the embeddings, metadatas or documents for provided ids, or create them if they don't exist.
    
    Args:
        input_data (Dict[str, Any]): Expected keys:
            "collection" (Collection): Collection to use.
            
            "ids": The ids of the embeddings to update.

            "embeddings": The embeddings to add. If None, embeddings will be computed based on the documents or images using the embedding_function set for the Collection. Optional.
            
            "metadatas": The metadata to associate with the embeddings. When querying, you can filter on this metadata. Optional.
            
            "documents": The documents to associate with the embeddings. Optional.
            
            "images": The images to associate with the embeddings. Optional.
            
            "uris": The uris of the images to associate with the embeddings. Optional.
    """
    def execute(self, input_data: Dict[str, Any]) -> None:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "collection" (Collection): Collection to use.
                
                "ids": The ids of the embeddings to update.

                "embeddings": The embeddings to add. If None, embeddings will be computed based on the documents or images using the embedding_function set for the Collection. Optional.
                
                "metadatas": The metadata to associate with the embeddings. When querying, you can filter on this metadata. Optional.
                
                "documents": The documents to associate with the embeddings. Optional.
                
                "images": The images to associate with the embeddings. Optional.
                
                "uris": The uris of the images to associate with the embeddings. Optional.
        """
        collection: Collection = input_data["collection"]
        collection.upsert( # type: ignore
            ids=input_data["ids"],
            embeddings=input_data.get("embeddings"),
            metadatas=input_data.get("metadatas"),
            documents=input_data.get("documents"),
            images=input_data.get("images"),
            uris=input_data.get("uris"),
        )


class ChromaDBCollectionQuery(Action[Dict[str, Any], QueryResult]):
    """
    Get the n_results nearest neighbor embeddings for provided query_embeddings or query_texts.

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "collection" (Collection): Collection to use.

            "query_embeddings": The embeddings to get the closes neighbors of. Optional.
            
            "query_texts": The document texts to get the closes neighbors of. Optional.
            
            "query_images": The images to get the closes neighbors of. Optional.
            
            "n_results": The number of neighbors to return for each query_embedding or query_texts. Optional.
            
            "where": A Where type dict used to filter results by. E.g. {"$and": ["color" : "red", "price": {"$gte": 4.20}]}. Optional.
            
            "where_document": A WhereDocument type dict used to filter by the documents. E.g. {$contains: {"text": "hello"}}. Optional.
            
            "include": A list of what to include in the results. Can contain "embeddings", "metadatas", "documents", "distances". Ids are always included. Defaults to ["metadatas", "documents", "distances"]. Optional.

    Returns:
        QueryResult: A QueryResult object containing the results.
    """
    def execute(self, input_data: Dict[str, Any]) -> QueryResult:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "collection" (Collection): Collection to use.

                "query_embeddings": The embeddings to get the closes neighbors of. Optional.
                
                "query_texts": The document texts to get the closes neighbors of. Optional.
                
                "query_images": The images to get the closes neighbors of. Optional.
                
                "n_results": The number of neighbors to return for each query_embedding or query_texts. Optional.
                
                "where": A Where type dict used to filter results by. E.g. {"$and": ["color" : "red", "price": {"$gte": 4.20}]}. Optional.
                
                "where_document": A WhereDocument type dict used to filter by the documents. E.g. {$contains: {"text": "hello"}}. Optional.
                
                "include": A list of what to include in the results. Can contain "embeddings", "metadatas", "documents", "distances". Ids are always included. Defaults to ["metadatas", "documents", "distances"]. Optional.

        Returns:
            QueryResult: A QueryResult object containing the results.
        """
        collection: Collection = input_data["collection"]
        return collection.query( # type: ignore
            query_embeddings=input_data.get("query_embeddings"),
            query_texts=input_data.get("query_texts"),
            query_uris=input_data.get("query_uris"),
            n_results=input_data.get("n_results", 10),
            where=input_data.get("where"),
            where_document=input_data.get("where_document"),
            include=input_data.get("include", ["metadatas", "documents", "distances"]),
        )
    

class ChromaDBCollectionGet(Action[Dict[str, Any], GetResult]):
    """
    Get embeddings and their associate data from the data store. If no ids or where filter is provided returns all embeddings up to limit starting at offset.

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "collection" (Collection): Collection to use.

            "ids": The ids of the embeddings to get. Optional.

            "where": A Where type dict used to filter results by. E.g. {"$and": ["color" : "red", "price": {"$gte": 4.20}]}. Optional.
            
            "limit": The number of documents to return. Optional.
            
            "offset": The offset to start returning results from. Useful for paging results with limit. Optional.
            
            "where_document": A WhereDocument type dict used to filter by the documents. E.g. {$contains: {"text": "hello"}}. Optional.
            
            "include": A list of what to include in the results. Can contain "embeddings", "metadatas", "documents". Ids are always included. Defaults to ["metadatas", "documents"]. Optional.

    Returns:
        GetResult: A GetResult object containing the results.
    """
    def execute(self, input_data: Dict[str, Any]) -> GetResult:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "collection" (Collection): Collection to use.

                "ids": The ids of the embeddings to get. Optional.

                "where": A Where type dict used to filter results by. E.g. {"$and": ["color" : "red", "price": {"$gte": 4.20}]}. Optional.
                
                "limit": The number of documents to return. Optional.
                
                "offset": The offset to start returning results from. Useful for paging results with limit. Optional.
                
                "where_document": A WhereDocument type dict used to filter by the documents. E.g. {$contains: {"text": "hello"}}. Optional.
                
                "include": A list of what to include in the results. Can contain "embeddings", "metadatas", "documents". Ids are always included. Defaults to ["metadatas", "documents"]. Optional.

        Returns:
            GetResult: A GetResult object containing the results.
        """
        collection: Collection = input_data["collection"]
        return collection.get( # type: ignore
            ids=input_data.get("ids"),
            limit=input_data.get("limit"),
            offset=input_data.get("offset"),
            where=input_data.get("where"),
            where_document=input_data.get("where_document"),
            include=input_data.get("include", ["metadatas", "documents"]),
        )

