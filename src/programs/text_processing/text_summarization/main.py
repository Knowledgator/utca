from core.executable_level_1.schema import Transformable

from implementation.tasks.text_processing.summarization.transformers.transformers_summarization import (
    SummarizationTask
)

task = SummarizationTask()

if __name__ == "__main__":
    with open("programs/text_processing/text_summarization/text.txt", "r") as f:
        text = f.read()
    print(task.execute(Transformable({
        "inputs": [text],
        "max_length": 200,
        "min_length": 100
    })).extract())