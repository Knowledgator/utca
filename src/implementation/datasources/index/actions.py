from typing import Any, Dict
from core.executable_level_1.actions import Action

import faiss # type: ignore

class BuildIndex(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(self, dataset_dimensions: int=1024):
        self.dataset_dimensions = dataset_dimensions


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data["index"] = faiss.IndexFlatL2(self.dataset_dimensions)
        return input_data
    

class AddDataset(Action[Dict[str, Any], Dict[str, Any]]):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data["index"].add(input_data["dataset"]) # type: ignore
        return input_data


class SearchIndex(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(self, results_count: int=1):
        self.results_count = results_count
    

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        index = input_data["index"]
        input_data["search_results"] = {}
        (
            input_data["search_results"]["distances"],
            input_data["search_results"]["indexes"]
        ) = index.search(input_data["query"], self.results_count)
        return input_data
    

class GetTextsByIndexes(Action[Dict[str, Any], Dict[str, Any]]):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data["search_results"]["texts"] = [
            input_data["texts"][i] 
            for query_res in input_data["search_results"]["indexes"]
            for i in query_res
        ]
        return input_data