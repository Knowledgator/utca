import pathlib
PATH = pathlib.Path(__file__).parent.resolve()

from core.executable_level_1.schema import Transformable
from implementation.tasks.text_processing.summarization.transformers.transformers_summarization import (
    SummarizationTask
)

task = SummarizationTask()

if __name__ == "__main__":
    with open(f"{PATH}/text.txt", "r") as f:
        text = f.read()
    print(task(Transformable({
        "inputs": text,
        "max_length": 200,
        "min_length": 100
    })).extract())