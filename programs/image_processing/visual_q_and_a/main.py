import pathlib
PATH = pathlib.Path(__file__).parent.resolve()

from utca.core import (
    AddData
)
from utca.implementation.tasks import (
    TransformersVisualQandA
)
from utca.implementation.datasources.image import ImageRead

task = TransformersVisualQandA()

if __name__ == "__main__":
    pipeline = (
        ImageRead()
        | AddData({"question": "How many cats are there?"})
        | task
    )

    print(pipeline.run({
        "path_to_file": f"{PATH}/test.jpg"
    }))