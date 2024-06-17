import uuid

from qdrant_client import QdrantClient

from utca.core import AddData, ReplacingScope
from utca.implementation.datasources.db import (
    QdrantAdd,
    QdrantQuery,
)

# Sentences for dataset
sentences = [
    "People who test positive for Covid-19 no longer need to routinely stay away from others for at least five days, according to new guidelines from the US Centers for Disease Control and Prevention issued Friday.", 
    "The change ends a strategy from earlier in the pandemic that experts said has been important to controlling the spread of the infection.",
    "Whether it be the latest prized Stanley cup or that 10-year-old plastic spout bottle you don’t go anywhere without, “emotional support water bottles” seem to be stuck to our sides and not going anywhere.",
    "Health officials in Alaska recently reported the first known human death from a virus called Alaskapox.",
    "Blizzard conditions continued to slam Northern California over the weekend with damaging winds and heavy snow dumping on mountain ridges down to the valleys.",
]

if __name__ == "__main__":
    qdrant_client = QdrantClient(":memory:")

    pipe = (
        AddData({
            "collection_name": "test",
            "documents": sentences,
            "ids": [str(uuid.uuid4()) for _ in range(len(sentences))]
        })
        | QdrantAdd(client=qdrant_client)
        | AddData({
            "query_text": "Bad weather",
            "limit": 1
        })
        | QdrantQuery(client=qdrant_client).use(set_key="results", replace=ReplacingScope.GLOBAL)
    )
    print(pipe.run()["results"])