from typing import Dict, Any, cast

import faiss # type: ignore
import numpy as np

from core.executable_level_1.schema import Transformable
from implementation.tasks.text_processing.embedding.transformers.transformers_embedding import (
    TextEmbeddingTask
)

task = TextEmbeddingTask()

# Sentences we want sentence embeddings for
sentences = [
    "People who test positive for Covid-19 no longer need to routinely stay away from others for at least five days, according to new guidelines from the US Centers for Disease Control and Prevention issued Friday.", 
    "The change ends a strategy from earlier in the pandemic that experts said has been important to controlling the spread of the infection.",
    "Whether it be the latest prized Stanley cup or that 10-year-old plastic spout bottle you don’t go anywhere without, “emotional support water bottles” seem to be stuck to our sides and not going anywhere.",
    "Health officials in Alaska recently reported the first known human death from a virus called Alaskapox.",
    "Blizzard conditions continued to slam Northern California over the weekend with damaging winds and heavy snow dumping on mountain ridges down to the valleys.",
]

if __name__ == "__main__":
    sentence_embeddings = task.execute(Transformable({
        "sentences": sentences
    })).extract()
    subject = cast(
        Dict[str, Any], 
        sentence_embeddings
    )["embeddings"]
    subject_np = np.array([
        s.detach().numpy() for s in subject
    ])

    query_embedding = task.execute(Transformable({
        "sentences": ["Bad weather"]
    })).extract()
    query = cast(
        Dict[str, Any], 
        query_embedding
    )["embeddings"]
    query_np = np.array([
        q.detach().numpy() for q in query
    ])

    index = faiss.IndexFlatL2(1024)
    index.add(subject_np)

    D, I = index.search(query_np, 5)     # actual search
    print(I) # indexex
    print(D) # distances
    
    print(f"About bad weather: {sentences[I[0][0]]}")