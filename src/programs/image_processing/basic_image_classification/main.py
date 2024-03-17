from implementation.tasks.image_processing.image_classification.transformers.transformers_image_classification import (
    TransformersImageClassification
)
from implementation.datasources.image.actions import (
    ImageRead,
)
from core.executable_level_1.interpreter import Evaluator

if __name__ == "__main__":
    pipeline = (
        ImageRead() | TransformersImageClassification()
    )

    result = Evaluator(pipeline).run_program({
        "path_to_file": "programs/image_processing/basic_image_classification/test.jpg" # Image of German Shepherd Dog
    })
    print(result)