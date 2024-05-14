import pathlib
PATH = pathlib.Path(__file__).parent.resolve()

from utca.core import (
    AddData
)
from utca.implementation.tasks import (
    TransformersDocumentQandA
)
from utca.implementation.datasources.image import ImageRead

if __name__ == "__main__":
    pipeline = (
        ImageRead()
        | AddData({
            "question": "What is the purchase amount?"
        })
        | TransformersDocumentQandA()
    )

    print(pipeline.run({
        "path_to_file": f"{PATH}/test.jpeg"
    }))