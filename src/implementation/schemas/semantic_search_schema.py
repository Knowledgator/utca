from __future__ import annotations
from typing import List, Optional, cast, Dict, Any

import numpy.typing as npt

from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import (
    Config, Input, Output, Transformable
)
from implementation.tasks.text_processing.embedding.transformers.transformers_embedding import (
    TextEmbeddingTask
)
from implementation.datasources.index.actions import (
    BuildIndex, AddDataset, SearchIndex, GetTextsByIndexes,
)

class SemanticSearchSchema(Executable[Config, Input, Output]):
    default_encoder = TextEmbeddingTask
    dataset: List[str]

    def __init__(
        self, 
        dataset: Optional[List[str]] = None, 
        encoder: Optional[TextEmbeddingTask]=None#Optional[Executable[Config, Input, Output]] = None,
    ) -> None:
        if encoder is None:
            encoder = self.default_encoder()
        self.encoder = encoder

        self.index = BuildIndex(
            encoder.predictor.config.hidden_size # type: ignore
        ).execute({})["index"]

        self.dataset = []
        if dataset:
            self.add(dataset)
    

    def get_embeddings(self, texts: List[str]) -> npt.NDArray[Any]:
        return cast(
            Dict[str, Any],
            self.encoder.execute(Transformable({
                "texts": texts
            })).extract()
        )["embeddings"]


    def add(self, dataset: List[str]) -> SemanticSearchSchema:
        embeddings = self.get_embeddings(dataset)
        self.dataset.extend(dataset)
        AddDataset().execute({
            "index": self.index,
            "dataset": embeddings
        })
        return self


    def invoke(self, input_data: Input) -> Dict[str, Any]:
        return {}
    
    
    def invoke_batch(self, input_data: List[Input]) -> List[Dict[str, Any]]:
        return []


    def execute(self, input_data: Transformable) -> Transformable:
        state = cast(Dict[str, Any], input_data.extract())
        query = state["query"]
        search_results = SearchIndex(state["results_count"]).execute({
            "query": self.get_embeddings([query]),
            "index": self.index
        })
        search_results = GetTextsByIndexes().execute(
            {
                **search_results,
                "texts": self.dataset
            }
        )
        return Transformable(search_results)
    

    def execute_batch(self, input_data: Transformable) -> Transformable:
        # temporary
        return Transformable([
            cast(
                Dict[str, Any],
                self.execute(Transformable(i)).extract()
            ) for i in input_data
        ])