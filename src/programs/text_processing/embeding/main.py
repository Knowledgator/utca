from typing import Dict, Any, cast

from core.executable_level_1.schema import Transformable
from implementation.tasks.text_processing.embedding.transformers.transformers_embedding import (
    TextEmbeddingTask
)

task = TextEmbeddingTask()

# Sentences we want sentence embeddings for
sentences = [
    "People who test positive for Covid-19 no longer need to routinely stay away from others for at least five days, according to new guidelines from the US Centers for Disease Control and Prevention issued Friday.", 
    "The change ends a strategy from earlier in the pandemic that experts said has been important to controlling the spread of the infection."
]

if __name__ == "__main__":
    sentence_embeddings = task.execute(Transformable({
        "sentences": sentences
    })).extract()

    print(cast(Dict[str, Any], sentence_embeddings)["embeddings"])