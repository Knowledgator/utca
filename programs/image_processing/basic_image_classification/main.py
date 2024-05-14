import pathlib
PATH = pathlib.Path(__file__).parent.resolve()

from utca.implementation.tasks import TransformersImageClassification
from utca.implementation.datasources.image import ImageRead

if __name__ == "__main__":
    pipeline = (
        ImageRead() | TransformersImageClassification()
    )

    result = pipeline.run({
        "path_to_file": f"{PATH}/test.jpg" # Image of German Shepherd Dog
    })
    print(result)