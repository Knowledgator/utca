from __future__ import annotations
from typing import  Any, Dict, List, Optional, Type

import numpy.typing as npt

from utca.core.executable_level_1.interpreter import Evaluator
from utca.core.executable_level_1.executable import Executable
from utca.core.executable_level_1.schema import IOModel
from utca.implementation.tasks.text_processing.embedding.transformers_task.transformers_embedding import (
    TransformersTextEmbedding
)
from utca.implementation.datasources.index.actions import (
    IndexCreate, IndexData, IndexSearch, GetTextsByIndexes,
)

class SemanticSearchSchemaInput(IOModel):
    query: List[str]
    results_count: int


class SemanticSearchSchemaOutput(IOModel):
    """
    Args:
        search_results (Dict[str, Any]): Expected keys:
            "distances" (List[float]): List of distances;

            "indexes" (List[Any]): Indexes of indexed data;
            
            "texts" (List[str]): Texts of results;
    """
    search_results: Dict[str, Any]


class SemanticSearchSchema(
    Executable[
        SemanticSearchSchemaInput, 
        SemanticSearchSchemaOutput
    ]
):
    """
    Schema for semantic search
    """
    def __init__(
        self, 
        dataset: Optional[List[str]]=None, 
        encoder: Optional[TransformersTextEmbedding[Any, Any]]=None,
        input_class: Type[SemanticSearchSchemaInput]=SemanticSearchSchemaInput,
        output_class: Type[SemanticSearchSchemaOutput]=SemanticSearchSchemaOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            dataset (Optional[List[str]], optional): Dataset for search. Defaults to None.
            
            encoder (Optional[TransformersTextEmbedding[Any, Any]], optional): Encoder for embeddings creation.
                If equals to None, default encoder will be used. Defaults to None.
            
            input_class (Type[SemanticSearchSchemaInput], optional): Class for input validation.
                Defaults to SemanticSearchSchemaInput.
            
            output_class (Type[SemanticSearchSchemaOutput], optional): Class for output validation.
                Defaults to SemanticSearchSchemaOutput.
           
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(
            input_class=input_class,
            output_class=output_class,
            name=name,
        )
        if encoder is None:
            encoder = TransformersTextEmbedding()
        self.encoder = encoder

        self.index = self.build_index()

        self.dataset: List[str] = []
        if dataset:
            self.add(dataset)
    

    def get_embeddings(self, texts: List[str]) -> npt.NDArray[Any]:
        return self.encoder.run({
                "texts": texts
            })["embeddings"]


    def add(self, dataset: List[str]) -> SemanticSearchSchema:
        """
        Add data to index
        """
        embeddings = self.get_embeddings(dataset)
        self.dataset.extend(dataset)
        IndexData().execute({
            "index": self.index,
            "dataset": embeddings
        })
        return self


    def build_index(self) -> Any:
        return IndexCreate(
            self.encoder.predictor.config.hidden_size # type: ignore
        ).execute({})["index"]


    def drop_index(self) -> Any:
        self.index = self.build_index()


    def invoke(self, input_data: SemanticSearchSchemaInput, evaluator: Evaluator) -> Dict[str, Any]:
        search_results = IndexSearch(input_data.results_count).execute({
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