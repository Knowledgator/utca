import pathlib
PATH = pathlib.Path(__file__).parent.resolve()

from utca.implementation.tasks import (
    TransformersTextSummarization
)

task = TransformersTextSummarization()

if __name__ == "__main__":
    with open(f"{PATH}/text.txt", "r") as f:
        text = f.read()
    print(task.run({
        "inputs": text,
        "max_length": 200,
        "min_length": 100
    }))