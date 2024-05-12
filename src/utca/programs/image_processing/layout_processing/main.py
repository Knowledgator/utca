import pathlib
PATH = pathlib.Path(__file__).parent.resolve()

from core import (
    AddData
)
from implementation.tasks import (
    TransformersDocumentQandA
)
from implementation.datasources.image import ImageRead

task = TransformersDocumentQandA()

if __name__ == "__main__":
    pipeline = (
        ImageRead()
        | AddData({
            "question": "What is the purchase amount?"
        })
        | task
    )

    print(pipeline.run({
        "path_to_file": f"{PATH}/test.jpeg"
    }))