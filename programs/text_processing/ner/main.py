from utca.implementation.tasks import (
    TransformersTokenClassifier
)

task = TransformersTokenClassifier()

if __name__ == "__main__":
    print(task.run({
        "inputs": "My name is Sarah and I live in London"
    }))