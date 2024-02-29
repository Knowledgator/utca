from typing import Dict, Any, cast

from transformers import ( # type: ignore
    AutoImageProcessor, 
    AutoModelForImageClassification,
)

from implementation.predictors.transformers.transformers_model import (
    TransformersModel,
    TransformersModelConfig
)
from implementation.tasks.image_classification.transformers_image_classification import (
    TransformersImageClassification
)
from implementation.tasks.image_classification.actions import (
    ImageClassificationPreprocessor,
    ImageClassificationPreprocessorConfig,
    ImageClassificationSingleLabelPostprocessor,
    ImageClassificationPostprocessorConfig
)
from implementation.datasources.image.actions import (
    ImageRead, ImagePad,
)
from core.executable_level_1.interpreter import Evaluator

if __name__ == "__main__":
    model_name = "facebook/deit-base-distilled-patch16-384"

    model = AutoModelForImageClassification.from_pretrained(model_name) # type: ignore
    processor = AutoImageProcessor.from_pretrained(model_name) # type: ignore
    labels = model.config.id2label # type: ignore

    # Define task stage
    task = TransformersImageClassification(
        predictor=TransformersModel(
            TransformersModelConfig(
                model=model
            )
        ),
        preprocess=[
            ImagePad(width=224, height=224),
            ImageClassificationPreprocessor(
                ImageClassificationPreprocessorConfig(
                    processor=processor # type: ignore
                )
            )
        ],
        postprocess=[
            ImageClassificationSingleLabelPostprocessor(
                ImageClassificationPostprocessorConfig(
                    labels=labels # type: ignore
                )
            )
        ]
    )

    pipeline = (
        ImageRead() | task
    )

    result = cast(Dict[str, Any], Evaluator(pipeline).run_program({
        "path_to_file": "programs/program4/test.jpg" # Image of German Shepherd Dog
    }))
    print(result)