from typing import Any, Dict, List, Optional, Union

from qdrant_client import QdrantClient
from qdrant_client.models import UpdateResult, QueryResponse, ScoredPoint

from utca.core.executable_level_1.actions import Action, ActionInput, ActionOutput

class QdrantAction(Action[ActionInput, ActionOutput]):
    def __init__(
        self, 
        client: QdrantClient,
        name: Optional[str]=None,
        default_key: str="output",
    ) -> None:
        """
        Args:
            client (QdrantClient): Qdrant client to use

            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.

            default_key (str, optional): Default key used for results that is not of type Dict.
                Defaults to "output".
        """
        super().__init__(name, default_key=default_key)
        self.client = client


class QdrantCreateCollection(QdrantAction[Dict[str, Any], bool]):
    """
    Create empty collection with given parameters

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "collection_name": Name of the collection to create.
            
            "vectors_config": Configuration of the vector storage. 
                Vector params contains size and distance for the vector storage. 
                If dict is passed, service will create a vector storage for each key in the dict.
                If single VectorParams is passed, service will create a single anonymous vector storage.
            
            "sparse_vectors_config": Configuration of the sparse vector storage.
                The service will create a sparse vector storage for each key in the dict.
            
            "shard_number": Number of shards in collection. Default is 1, minimum is 1.
            
            "sharding_method": Defines strategy for shard creation. Option auto (default) creates defined number of shards automatically.
                Data will be distributed between shards automatically. 
                After creation, shards could be additionally replicated, but new shards could not be created.
                Option custom allows to create shards manually, each shard should be created with assigned unique shard_key. 
                Data will be distributed between based on shard_key value.
            
            "replication_factor": Replication factor for collection. Default is 1, minimum is 1. 
                Defines how many copies of each shard will be created. Have effect only in distributed mode.
            
            "write_consistency_factor": Write consistency factor for collection. Default is 1, minimum is 1. 
                Defines how many replicas should apply the operation for us to consider it successful. Increasing this number will make the collection more resilient to inconsistencies, but will also make it fail if not enough replicas are available. Does not have any performance impact. Have effect only in distributed mode.
            
            "on_disk_payload": If true - point`s payload will not be stored in memory. 
                It will be read from the disk every time it is requested.
                This setting saves RAM by (slightly) increasing the response time. 
                
                Note: those payload values that are involved in filtering and are indexed - remain in RAM.
            
            "hnsw_config": Params for HNSW index optimizers_config: 
                Params for optimizer wal_config: 
                Params for Write-Ahead-Log quantization_config: 
                Params for quantization, if None - quantization will be disabled init_from: 
                Use data stored in another collection to initialize this collection timeout:
                Wait for operation commit timeout in seconds. 
                If timeout is reached - request will return with service error.

    Returns:
        bool: Operation result.
    """
    def execute(self, input_data: Dict[str, Any]) -> bool:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "collection_name": Name of the collection to create.
                
                "vectors_config": Configuration of the vector storage. 
                    Vector params contains size and distance for the vector storage. 
                    If dict is passed, service will create a vector storage for each key in the dict.
                    If single VectorParams is passed, service will create a single anonymous vector storage.
                
                "sparse_vectors_config": Configuration of the sparse vector storage.
                    The service will create a sparse vector storage for each key in the dict.
                
                "shard_number": Number of shards in collection. Default is 1, minimum is 1.
                
                "sharding_method": Defines strategy for shard creation. Option auto (default) creates defined number of shards automatically.
                    Data will be distributed between shards automatically. 
                    After creation, shards could be additionally replicated, but new shards could not be created.
                    Option custom allows to create shards manually, each shard should be created with assigned unique shard_key. 
                    Data will be distributed between based on shard_key value.
                
                "replication_factor": Replication factor for collection. Default is 1, minimum is 1. 
                    Defines how many copies of each shard will be created. Have effect only in distributed mode.
                
                "write_consistency_factor": Write consistency factor for collection. Default is 1, minimum is 1. 
                    Defines how many replicas should apply the operation for us to consider it successful. Increasing this number will make the collection more resilient to inconsistencies, but will also make it fail if not enough replicas are available. Does not have any performance impact. Have effect only in distributed mode.
                
                "on_disk_payload": If true - point`s payload will not be stored in memory. 
                    It will be read from the disk every time it is requested.
                    This setting saves RAM by (slightly) increasing the response time. 
                    
                    Note: those payload values that are involved in filtering and are indexed - remain in RAM.
                
                "hnsw_config": Params for HNSW index optimizers_config: 
                    Params for optimizer wal_config: 
                    Params for Write-Ahead-Log quantization_config: 
                    Params for quantization, if None - quantization will be disabled init_from: 
                    Use data stored in another collection to initialize this collection timeout:
                    Wait for operation commit timeout in seconds. 
                    If timeout is reached - request will return with service error.

        Returns:
            bool: Operation result.
        """
        return self.client.create_collection(
            collection_name=input_data["collection_name"],
            vectors_config=input_data["vectors_config"],
            sparse_vectors_config=input_data.get("sparse_vectors_config"),
            shard_number=input_data.get("shard_number"),
            sharding_method=input_data.get("sharding_method"),
            replication_factor=input_data.get("replication_factor"),
            write_consistency_factor=input_data.get("write_consistency_factor"),
            on_disk_payload=input_data.get("on_disk_payload"),
            hnsw_config=input_data.get("hnsw_config"),
            optimizers_config=input_data.get("optimizers_config"),
            wal_config=input_data.get("wal_config"),
            quantization_config=input_data.get("quantization_config"),
            init_from=input_data.get("init_from"),
            timeout=input_data.get("timeout"),
            **(input_data.get("kwargs", {})),
        )
    

class QdrantRecreateCollection(QdrantAction[Dict[str, Any], bool]):
    """
    Delete and create empty collection with given parameters

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "collection_name": Name of the collection to recreate.
            
            "vectors_config": Configuration of the vector storage. 
                Vector params contains size and distance for the vector storage. 
                If dict is passed, service will create a vector storage for each key in the dict.
                If single VectorParams is passed, service will create a single anonymous vector storage.
            
            "sparse_vectors_config": Configuration of the sparse vector storage.
                The service will create a sparse vector storage for each key in the dict.
            
            "shard_number": Number of shards in collection. Default is 1, minimum is 1.
            
            "sharding_method": Defines strategy for shard creation. Option auto (default) creates defined number of shards automatically.
                Data will be distributed between shards automatically. 
                After creation, shards could be additionally replicated, but new shards could not be created.
                Option custom allows to create shards manually, each shard should be created with assigned unique shard_key. 
                Data will be distributed between based on shard_key value.
            
            "replication_factor": Replication factor for collection. Default is 1, minimum is 1. 
                Defines how many copies of each shard will be created. Have effect only in distributed mode.
            
            "write_consistency_factor": Write consistency factor for collection. Default is 1, minimum is 1. 
                Defines how many replicas should apply the operation for us to consider it successful. Increasing this number will make the collection more resilient to inconsistencies, but will also make it fail if not enough replicas are available. Does not have any performance impact. Have effect only in distributed mode.
            
            "on_disk_payload": If true - point`s payload will not be stored in memory. 
                It will be read from the disk every time it is requested.
                This setting saves RAM by (slightly) increasing the response time. 
                
                Note: those payload values that are involved in filtering and are indexed - remain in RAM.
            
            "hnsw_config": Params for HNSW index optimizers_config: 
                Params for optimizer wal_config: 
                Params for Write-Ahead-Log quantization_config: 
                Params for quantization, if None - quantization will be disabled init_from: 
                Use data stored in another collection to initialize this collection timeout:
                Wait for operation commit timeout in seconds. 
                If timeout is reached - request will return with service error.

    Returns:
        bool: Operation result.
    """
    def execute(self, input_data: Dict[str, Any]) -> bool:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "collection_name": Name of the collection to recreate.
                
                "vectors_config": Configuration of the vector storage. 
                    Vector params contains size and distance for the vector storage. 
                    If dict is passed, service will create a vector storage for each key in the dict.
                    If single VectorParams is passed, service will create a single anonymous vector storage.
                
                "sparse_vectors_config": Configuration of the sparse vector storage.
                    The service will create a sparse vector storage for each key in the dict.
                
                "shard_number": Number of shards in collection. Default is 1, minimum is 1.
                
                "sharding_method": Defines strategy for shard creation. Option auto (default) creates defined number of shards automatically.
                    Data will be distributed between shards automatically. 
                    After creation, shards could be additionally replicated, but new shards could not be created.
                    Option custom allows to create shards manually, each shard should be created with assigned unique shard_key. 
                    Data will be distributed between based on shard_key value.
                
                "replication_factor": Replication factor for collection. Default is 1, minimum is 1. 
                    Defines how many copies of each shard will be created. Have effect only in distributed mode.
                
                "write_consistency_factor": Write consistency factor for collection. Default is 1, minimum is 1. 
                    Defines how many replicas should apply the operation for us to consider it successful. Increasing this number will make the collection more resilient to inconsistencies, but will also make it fail if not enough replicas are available. Does not have any performance impact. Have effect only in distributed mode.
                
                "on_disk_payload": If true - point`s payload will not be stored in memory. 
                    It will be read from the disk every time it is requested.
                    This setting saves RAM by (slightly) increasing the response time. 
                    
                    Note: those payload values that are involved in filtering and are indexed - remain in RAM.
                
                "hnsw_config": Params for HNSW index optimizers_config: 
                    Params for optimizer wal_config: 
                    Params for Write-Ahead-Log quantization_config: 
                    Params for quantization, if None - quantization will be disabled init_from: 
                    Use data stored in another collection to initialize this collection timeout:
                    Wait for operation commit timeout in seconds. 
                    If timeout is reached - request will return with service error.

        Returns:
            bool: Operation result.
        """
        return self.client.recreate_collection(
            collection_name=input_data["collection_name"],
            vectors_config=input_data["vectors_config"],
            sparse_vectors_config=input_data.get("sparse_vectors_config"),
            shard_number=input_data.get("shard_number"),
            sharding_method=input_data.get("sharding_method"),
            replication_factor=input_data.get("replication_factor"),
            write_consistency_factor=input_data.get("write_consistency_factor"),
            on_disk_payload=input_data.get("on_disk_payload"),
            hnsw_config=input_data.get("hnsw_config"),
            optimizers_config=input_data.get("optimizers_config"),
            wal_config=input_data.get("wal_config"),
            quantization_config=input_data.get("quantization_config"),
            init_from=input_data.get("init_from"),
            timeout=input_data.get("timeout"),
            **(input_data.get("kwargs", {})),
        )


class QdrantDeleteCollection(QdrantAction[Dict[str, Any], bool]):
    """
    Remove collection and all it's data

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "collection_name": Name of the collection to delete.
            
            "timeout": Wait for operation commit timeout in seconds.
                If timeout is reached - request will return with service error.

            "kwargs": extra parameters.

    Returns:
        bool: Operation result
    """
    def execute(self, input_data: Dict[str, Any]) -> bool:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "collection_name": Name of the collection to delete.
                
                "timeout": Wait for operation commit timeout in seconds.
                    If timeout is reached - request will return with service error.

                "kwargs": extra parameters.

        Returns:
            bool: Operation result
        """
        return self.client.delete_collection(
            collection_name=input_data["collection_name"],
            timeout=input_data.get("timeout"),
            **(input_data.get("kwargs", {})),
        )


class QdrantAdd(QdrantAction[Dict[str, Any], List[Union[str, int]]]):
    """
    Adds text documents into qdrant collection. If collection does not exist, 
    it will be created with default parameters. Metadata in combination with documents 
    will be added as payload. Documents will be embedded using the specified embedding model.

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "collection_name" (str): Name of the collection to add documents to.

            "documents" (Iterable[str]): List of documents to embed and add to the collection.
            
            "metadata" (Iterable[Dict[str, Any]], optional): List of metadata dicts. Defaults to None.
            
            "ids" (Iterable[models.ExtendedPointId], optional): List of ids to assign to documents.
                If not specified, UUIDs will be generated. Defaults to None.
            
            "batch_size" (int, optional): How many documents to embed and upload in single request.
                Defaults to 32.
            
            "parallel" (Optional[int], optional): How many parallel workers to use for embedding.
                Defaults to None. If number is specified, data-parallel process will be used.
    
    Returns:
        List[Union[str, int]]: List of IDs of added documents. 
            If no ids provided, UUIDs will be randomly generated on client side.
    """
    def execute(self, input_data: Dict[str, Any]) -> List[Union[str, int]]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "collection_name" (str): Name of the collection to add documents to.

                "documents" (Iterable[str]): List of documents to embed and add to the collection.
                
                "metadata" (Iterable[Dict[str, Any]], optional): List of metadata dicts. Defaults to None.
                
                "ids" (Iterable[models.ExtendedPointId], optional): List of ids to assign to documents.
                    If not specified, UUIDs will be generated. Defaults to None.
                
                "batch_size" (int, optional): How many documents to embed and upload in single request.
                    Defaults to 32.
                
                "parallel" (Optional[int], optional): How many parallel workers to use for embedding.
                    Defaults to None. If number is specified, data-parallel process will be used.
        
        Returns:
            List[Union[str, int]]: List of IDs of added documents. 
                If no ids provided, UUIDs will be randomly generated on client side.
        """
        return self.client.add(
            collection_name=input_data["collection_name"],
            documents=input_data["documents"],
            metadata=input_data.get("metadata"),
            ids=input_data.get("ids"),
            batch_size=input_data.get("batch_size", 32),
            parallel=input_data.get("parallel")
        )


class QdrantUpsert(QdrantAction[Dict[str, Any], UpdateResult]):
    """
    Update or insert a new point into the collection.
    If point with given ID already exists - it will be overwritten.

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "collection_name" (str): To which collection to insert.
            
            "points" (Point): Batch or list of points to insert.
            
            "wait" (bool): Await for the results to be processed.
                - If True, result will be returned only when all changes are applied
                - If False, result will be returned immediately after the confirmation of receiving.
            
            "ordering" (Optional[WriteOrdering]): Define strategy for ordering of the points. Possible values:
                - `weak` (default) - write operations may be reordered, works faster
                - `medium` - write operations go through dynamically selected leader, may be inconsistent for a short period of time in case of leader change
                - `strong` - Write operations go through the permanent leader, consistent, but may be unavailable if leader is down
            
            "shard_key_selector": Defines the shard groups that should be used to write updates into. 
                If multiple shard_keys are provided, the update will be written to each of them. 
                Only works for collections with custom sharding method.

    Returns:
        UpdateResult: Operation result.
    """
    def execute(self, input_data: Dict[str, Any]) -> UpdateResult:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "collection_name" (str): To which collection to insert.
                
                "points" (Point): Batch or list of points to insert.
                
                "wait" (bool): Await for the results to be processed.
                    - If True, result will be returned only when all changes are applied
                    - If False, result will be returned immediately after the confirmation of receiving.
                
                "ordering" (Optional[WriteOrdering]): Define strategy for ordering of the points. Possible values:
                    - `weak` (default) - write operations may be reordered, works faster
                    - `medium` - write operations go through dynamically selected leader, may be inconsistent for a short period of time in case of leader change
                    - `strong` - Write operations go through the permanent leader, consistent, but may be unavailable if leader is down
                
                "shard_key_selector": Defines the shard groups that should be used to write updates into. 
                    If multiple shard_keys are provided, the update will be written to each of them. 
                    Only works for collections with custom sharding method.

        Returns:
            UpdateResult: Operation result.
        """
        return self.client.upsert(
            collection_name=input_data["collection_name"],
            points=input_data["points"],
            wait=input_data.get("wait", True),
            ordering=input_data.get("ordering"),
            shard_key_selector=input_data.get("shard_key_selector"),
            **(input_data.get("kwargs", {})),
        )
    

class QdrantDelete(QdrantAction[Dict[str, Any], UpdateResult]):
    """
    Delete selected points from collection

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "collection_name" (str): Name of the collection.
            
            "points_selector": Selects points based on list of IDs or filter. Examples:
                - `points=[1, 2, 3, "cd3b53f0-11a7-449f-bc50-d06310e7ed90"]`
                - `points=Filter(must=[FieldCondition(key='rand_number', range=Range(gte=0.7))])`
            
            "wait" (bool): Await for the results to be processed.
                - If True, result will be returned only when all changes are applied
                - If False, result will be returned immediately after the confirmation of receiving.
            
            "ordering" (Optional[WriteOrdering]): Define strategy for ordering of the points. Possible values:
                - `weak` (default) - write operations may be reordered, works faster
                - `medium` - write operations go through dynamically selected leader, may be inconsistent for a short period of time in case of leader change
                - `strong` - Write operations go through the permanent leader, consistent, but may be unavailable if leader is down
            
            "shard_key_selector": Defines the shard groups that should be used to write updates into. 
                If multiple shard_keys are provided, the update will be written to each of them. 
                Only works for collections with custom sharding method.

    Returns:
        UpdateResult: Operation result.
    """
    def execute(self, input_data: Dict[str, Any]) -> UpdateResult:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "collection_name" (str): Name of the collection.
                
                "points_selector": Selects points based on list of IDs or filter. Examples:
                    - `points=[1, 2, 3, "cd3b53f0-11a7-449f-bc50-d06310e7ed90"]`
                    - `points=Filter(must=[FieldCondition(key='rand_number', range=Range(gte=0.7))])`
                
                "wait" (bool): Await for the results to be processed.
                    - If True, result will be returned only when all changes are applied
                    - If False, result will be returned immediately after the confirmation of receiving.
                
                "ordering" (Optional[WriteOrdering]): Define strategy for ordering of the points. Possible values:
                    - `weak` (default) - write operations may be reordered, works faster
                    - `medium` - write operations go through dynamically selected leader, may be inconsistent for a short period of time in case of leader change
                    - `strong` - Write operations go through the permanent leader, consistent, but may be unavailable if leader is down
                
                "shard_key_selector": Defines the shard groups that should be used to write updates into. 
                    If multiple shard_keys are provided, the update will be written to each of them. 
                    Only works for collections with custom sharding method.

        Returns:
            UpdateResult: Operation result.
        """
        return self.client.delete(
            collection_name=input_data["collection_name"],
            points_selector=input_data["points_selector"],
            wait=input_data.get("wait", True),
            ordering=input_data.get("ordering"),
            shard_key_selector=input_data.get("shard_key_selector"),
            **(input_data.get("kwargs", {})),
        )


class QdrantQuery(QdrantAction[Dict[str, Any], List[QueryResponse]]):
    """
    Search for documents in a collection. This method automatically embeds the query text using the specified embedding model.
    If you want to use your own query vector, use search method instead.

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "collection_name": Collection to search in.
            
            "query_text": Text to search for. This text will be embedded using the specified embedding model. And then used as a query vector.
            
            "query_filter": Exclude vectors which doesn't fit given conditions. If None - search among all vectors 
            
            "limit": How many results return.
            
            "kwargs": Additional search parameters. See qdrant_client.models.SearchRequest for details.

    Returns:
        List[QueryResponse]: List of scored points.
    """
    def execute(self, input_data: Dict[str, Any]) -> List[QueryResponse]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "collection_name": Collection to search in.
                
                "query_text": Text to search for. This text will be embedded using the specified embedding model. And then used as a query vector.
                
                "query_filter": Exclude vectors which doesn't fit given conditions. If None - search among all vectors 
                
                "limit": How many results return.
                
                "kwargs": Additional search parameters.
        Returns:
            List[QueryResponse]: List of scored points.
        """
        return self.client.query(
            collection_name=input_data["collection_name"],
            query_text=input_data["query_text"],
            query_filter=input_data.get("query_filter"),
            limit=input_data.get("limit", 10),
            **(input_data.get("kwargs", {})),
        )
    

class QdrantSearch(QdrantAction[Dict[str, Any], List[ScoredPoint]]):
    """
    Search for closest vectors in collection taking into account filtering conditions

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "collection_name": Collection to search in.
            
            "query_vector": Search for vectors closest to this. Can be either a vector itself, 
                or a named vector, or a named sparse vector, or a tuple of vector name and vector itself
            
            "query_filter": Exclude vectors which doesn't fit given conditions. If None - search among all vectors 
            
            "search_params": Additional search params. 
            
            "limit": How many results return.
            
            "offset": Offset of the first result to return. May be used to paginate results. 
            
                Note: large offset values may cause performance issues. 
                
            "with_payload": Specify which stored payload should be attached to the result.
                If True - attach all payload. If False - do not attach any payload.
                If List of string - include only specified fields.
                If PayloadSelector - use explicit rules 
                
            "with_vectors": If True - Attach stored vector to the search result.
                If False - Do not attach vector. If List of string - include only specified fields.
                Defaults to False.
            
            "score_threshold": Define a minimal score threshold for the result. 
                If defined, less similar results will not be returned. 
                Score of the returned result might be higher or smaller 
                than the threshold depending on the Distance function used. 
                E.g. for cosine similarity only higher scores will be returned. 
            
            "consistency": Read consistency of the search. Defines how many 
                replicas should be queried before returning the result. 
                
                Values:
                - int - number of replicas to query, values should present in all queried replicas
                - 'majority' - query all replicas, but return values present in the majority of replicas
                - 'quorum' - query the majority of replicas, return values present in all of them
                - 'all' - query all replicas, and return values present in all replicas
            
            "shard_key_selector": This parameter allows to specify which shards should be queried. 
                If None - query all shards. Only works for collections with custom sharding method. 
            
            "timeout": Overrides global timeout for this search. Unit is seconds.

    Returns:
        List[ScoredPoint]: List of found close points with similarity scores.
    """
    def execute(self, input_data: Dict[str, Any]) -> List[ScoredPoint]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "collection_name": Collection to search in.
                
                "query_vector": Search for vectors closest to this. Can be either a vector itself, 
                    or a named vector, or a named sparse vector, or a tuple of vector name and vector itself
                
                "query_filter": Exclude vectors which doesn't fit given conditions. If None - search among all vectors 
                
                "search_params": Additional search params. 
                
                "limit": How many results return.
                
                "offset": Offset of the first result to return. May be used to paginate results. 
                
                    Note: large offset values may cause performance issues. 
                    
                "with_payload": Specify which stored payload should be attached to the result.
                    If True - attach all payload. If False - do not attach any payload.
                    If List of string - include only specified fields.
                    If PayloadSelector - use explicit rules 
                    
                "with_vectors": If True - Attach stored vector to the search result.
                    If False - Do not attach vector. If List of string - include only specified fields.
                    Defaults to False.
                
                "score_threshold": Define a minimal score threshold for the result. 
                    If defined, less similar results will not be returned. 
                    Score of the returned result might be higher or smaller 
                    than the threshold depending on the Distance function used. 
                    E.g. for cosine similarity only higher scores will be returned. 
                
                "consistency": Read consistency of the search. Defines how many 
                    replicas should be queried before returning the result. 
                    
                    Values:
                    - int - number of replicas to query, values should present in all queried replicas
                    - 'majority' - query all replicas, but return values present in the majority of replicas
                    - 'quorum' - query the majority of replicas, return values present in all of them
                    - 'all' - query all replicas, and return values present in all replicas
                
                "shard_key_selector": This parameter allows to specify which shards should be queried. 
                    If None - query all shards. Only works for collections with custom sharding method. 
                
                "timeout": Overrides global timeout for this search. Unit is seconds.

        Returns:
            List[ScoredPoint]: List of found close points with similarity scores.
        """
        return self.client.search(
            collection_name=input_data["collection_name"],
            query_vector=input_data["query_vector"],
            query_filter=input_data.get("query_filter"),
            search_params=input_data.get("search_params"),
            limit=input_data.get("limit", 10),
            offset=input_data.get("offset"),
            with_payload=input_data.get("with_payload", True),
            with_vectors=input_data.get("with_vectors", False),
            score_threshold=input_data.get("score_threshold"),
            consistency=input_data.get("consistency"),
            shard_key_selector=input_data.get("shard_key_selector"),
            timeout=input_data.get("timeout"),
            **(input_data.get("kwargs", {})),
        )