from typing import Any, Dict, Optional
import importlib.util

from utca.core.executable_level_1.actions import Action

class IndexCreate(Action[Any, Dict[str, Any]]):
    """
    Create FAISS index

    Args:
        input_data (Any): Ignored.

    Returns:
        Dict[str, Any]: Expected keys:
            'index' (faiss.IndexFlatL2): Created index.
    """
    def __init__(
        self, 
        dataset_dimensions: int=1024,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            dataset_dimensions (int, optional): Dataset dimension. Defaults to 1024.

            name (Optional[str], optional): name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        if not importlib.util.find_spec("faiss"):
            raise ImportError("To use index FAISS required. To install faiss package use:\npip install faiss-cpu\nOR\npip install faiss-gpu")
        super().__init__(name)
        self.dataset_dimensions = dataset_dimensions


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Any): Ignored.

        Returns:
            Dict[str, Any]: Expected keys:
                'index' (faiss.IndexFlatL2): Created index.
        """
        import faiss # type: ignore
        return {
            "index": faiss.IndexFlatL2(self.dataset_dimensions)
        }
    

class IndexData(Action[Dict[str, Any], None]):
    """
    Index data
    """
    def execute(self, input_data: Dict[str, Any]) -> None:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'index' (faiss.IndexFlatL2): Index to update;

                'dataset' (Any): Data to index;
        """
        input_data["index"].add(input_data["dataset"]) # type: ignore


class IndexSearch(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Search index
    """
    def __init__(self, results_count: int=1, name: Optional[str]=None) -> None:
        """
        Args:
            results_count (int, optional): How many results to return. Defaults to 1.
           
            name (Optional[str], optional): name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.results_count = results_count
    

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'index' (faiss.IndexFlatL2): Index to search;

                'query' (Any): Query to search;

        Returns:
            Dict[str, Any]: Expected keys:
                'search_results' (Dict[str, Any]): Results of search. Results include:
                    'distances' (List[float]): List of distances;

                    'indexes' (List[Any]): Indexes of indexed data;
        """
        index = input_data["index"]
        search_results = {}
        (
            search_results["distances"],
            search_results["indexes"]
        ) = index.search(input_data["query"], self.results_count)
        return {
            "search_results": search_results 
        }
    

class GetTextsByIndexes(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Get texts from resulted indexes
    """
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'texts' (List[str]): Indexed texts;

                'search_results' (Dict[str, Any]): Results of search. Results include:
                    'distances' (List[float]): List of distances;

                    'indexes' (List[Any]): Indexes of indexed data;

        Returns:
            Dict[str, Any]: Expected keys:
                'search_results' (Dict[str, Any]): Results of search. Results include:
                    'distances' (List[float]): List of distances;

                    'indexes' (List[Any]): Indexes of indexed data;

                    'texts' (List[str]): Texts of results;
        """
        return {
            "search_results": {
                **input_data["search_results"],
                "texts": [
                    input_data["texts"][i] 
                    for query_res in input_data["search_results"]["indexes"]
                    for i in query_res
                ]
            }
        }