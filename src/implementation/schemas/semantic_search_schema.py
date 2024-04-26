from __future__ import annotations
from typing import  Any, Dict, List, Optional, Type

import numpy.typing as npt

from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import (
    IOModel, Transformable
)
from implementation.tasks.text_processing.embedding.transformers.transformers_embedding import (
    TextEmbedding
)
from implementation.datasources.index.actions import (
    CreateIndex, IndexData, SearchIndex, GetTextsByIndexes,
)

class SemanticSearchSchemaInput(IOModel):
    query: List[str]
    results_count: int


class SemanticSearchSchemaOutput(IOModel):
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
        encoder: Optional[TextEmbedding]=None,
        input_class: Type[SemanticSearchSchemaInput]=SemanticSearchSchemaInput,
        output_class: Type[SemanticSearchSchemaOutput]=SemanticSearchSchemaOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            dataset (Optional[List[str]], optional): Dataset for search. Defaults to None.
            
            encoder (Optional[TextEmbedding], optional): Encoder for embeddings creation.
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
            encoder = TextEmbedding()
        self.encoder = encoder

        self.index = self.build_index()

        self.dataset: List[str] = []
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
        return CreateIndex(
            self.encoder.predictor.config.hidden_size # type: ignore
        ).execute({})["index"]


    def drop_index(self) -> Any:
        self.index = self.build_index()


    def invoke(self, input_data: SemanticSearchSchemaInput, evaluator: Evaluator) -> Dict[str, Any]:
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