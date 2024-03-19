from core.executable_level_1.schema import Transformable
from implementation.tasks.text_processing.ner.transformers.transformers_token_classification import (
    TokenClassifierTask
)

task = TokenClassifierTask()

if __name__ == "__main__":
    print(task(Transformable({
        "inputs": "My name is Sarah and I live in London"
    })).extract())