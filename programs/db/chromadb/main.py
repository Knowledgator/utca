from chromadb import PersistentClient, Documents, Embeddings

from utca.core import AddData, ReplacingScope
from utca.implementation.tasks import TransformersTextEmbedding
from utca.implementation.datasources.db import (
    ChromaDBGetOrCreateCollection,
    ChromaDBCollectionAddData,
    ChromaDBEmbeddingFunctionComponent,
    ChromaDBCollectionQuery,
)

# Sentences for dataset
sentences = [
    "People who test positive for Covid-19 no longer need to routinely stay away from others for at least five days, according to new guidelines from the US Centers for Disease Control and Prevention issued Friday.", 
    "The change ends a strategy from earlier in the pandemic that experts said has been important to controlling the spread of the infection.",
    "Whether it be the latest prized Stanley cup or that 10-year-old plastic spout bottle you don’t go anywhere without, “emotional support water bottles” seem to be stuck to our sides and not going anywhere.",
    "Health officials in Alaska recently reported the first known human death from a virus called Alaskapox.",
    "Blizzard conditions continued to slam Northern California over the weekend with damaging winds and heavy snow dumping on mountain ridges down to the valleys.",
]

embedding_pipe = TransformersTextEmbedding()
class EmbeddingFunction(ChromaDBEmbeddingFunctionComponent[Documents]):
    def __call__(self, documents: Documents) -> Embeddings:
        return embedding_pipe.run({"texts": documents})["embeddings"].tolist()

pipe = (
    AddData({
        "collection_name": "test",
    })
    | ChromaDBGetOrCreateCollection(
        client=PersistentClient(), embedding_function=EmbeddingFunction(embedding_pipe) # type: ignore
    ).use(get_key="collection_name")
    | AddData({
        "documents": sentences,
        "ids": [f"id_{i}" for i in range(1, len(sentences)+1)]
    })
    | ChromaDBCollectionAddData()
    | AddData({
        "query_texts": ["Bad weather"],
        "n_results": 1,
        "include": ["documents", "distances"]
    })
    | ChromaDBCollectionQuery().use(set_key="results", replace=ReplacingScope.GLOBAL)
)

if __name__ == "__main__":
    print(pipe.run()["results"])