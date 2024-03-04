from typing import Any, Dict
from core.executable_level_1.actions import OneToOne

import faiss # type: ignore

class BuildIndex(OneToOne):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        index = faiss.IndexFlatL2(input_data["dataset_dimensions"])
        index.add(input_data["dataset"]) # type: ignore
        input_data["index"] = index
        return input_data
    

class SearchIndex(OneToOne):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        index = input_data["index"]
        input_data["search_results"] = {}
        (
            input_data["search_results"]["distances"],
            input_data["search_results"]["indexes"]
        ) = index.search(input_data["query"], input_data["k"])
        return input_data
    

class GetTextsByIndexes(OneToOne):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data["search_results"]["texts"] = [
            input_data["texts"][i] 
            for query_res in input_data["search_results"]["indexes"]
            for i in query_res
        ]
        return input_data