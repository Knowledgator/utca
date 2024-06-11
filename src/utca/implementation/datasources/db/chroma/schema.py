from abc import abstractmethod

from chromadb import EmbeddingFunction, Embeddings
from chromadb.api.types import D

from utca.core.executable_level_1.component import Component

class ChromaDBEmbeddingFunctionComponent(EmbeddingFunction[D]):
    """
    Embedding function wrapper for components
    """
    def __init__(self, component: Component) -> None:
        super().__init__()
        self.component = component
        

    
    @abstractmethod
    def __call__(self, input: D) -> Embeddings:
        ...