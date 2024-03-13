from __future__ import annotations
from typing import List, Optional, Dict, Any

import numpy.typing as npt

from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import (
    Input, Output, Transformable
)
from implementation.tasks.text_processing.embedding.transformers.transformers_embedding import (
    TextEmbeddingTask
)
from implementation.datasources.index.actions import (
    BuildIndex, AddDataset, SearchIndex, GetTextsByIndexes,
)

class SemanticSearchSchemaInput(Input):
    query: List[str]
    results_count: int


class SemanticSearchSchemaOutput(Output):
    search_results: Dict[str, Any]


class SemanticSearchSchema(
    Executable[
        SemanticSearchSchemaInput, 
        SemanticSearchSchemaOutput
    ]
):
    input_class = SemanticSearchSchemaInput
    output_class = SemanticSearchSchemaOutput
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

        self.index = self.build_index()

        self.dataset = []
        if dataset:
            self.add(dataset)
    

    def get_embeddings(self, texts: List[str]) -> npt.NDArray[Any]:
        return getattr(
            self.encoder(Transformable({
                "texts": texts
            })), 
            "embeddings"
        )


    def add(self, dataset: List[str]) -> SemanticSearchSchema:
        embeddings = self.get_embeddings(dataset)
        self.dataset.extend(dataset)
        AddDataset().execute({
            "index": self.index,
            "dataset": embeddings
        })
        return self


    def build_index(self) -> Any:
        return BuildIndex(
            self.encoder.predictor.config.hidden_size # type: ignore
        ).execute({})["index"]


    def drop_index(self) -> Any:
        self.index = self.build_index()


    def invoke(self, input_data: SemanticSearchSchemaInput) -> Dict[str, Any]:
        search_results = SearchIndex(input_data.results_count).execute({
            "query": self.get_embeddings(input_data.query),
            "index": self.index
        })
        search_results = GetTextsByIndexes().execute(
            {
                **search_results,
                "texts": self.dataset
            }
        )
        return search_results
    
    
    def invoke_batch(self, input_data: List[SemanticSearchSchemaInput]) -> List[Dict[str, Any]]:
        return [
            self.invoke(i) for i in input_data 
        ]