from transformers import ( # type: ignore
    ViltProcessor, ViltForQuestionAnswering
)

from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.actions import (
    AddData
)
from implementation.predictors.transformers.transformers_model import (
    TransformersModel,
    TransformersModelConfig
)
from implementation.tasks.visual_q_and_a.transformers_visual_q_and_a import (
    TransformersVisualQandA
)
from implementation.tasks.visual_q_and_a.actions import (
    VisualQandAPreprocessor,
    VisualQandAPreprocessorConfig,
    VisualQandAPostprocessor,
    VisualQandAPostprocessorConfig
)
from implementation.datasources.image.actions import ImageRead

model_name = "dandelin/vilt-b32-finetuned-vqa"

model = ViltForQuestionAnswering.from_pretrained(model_name) # type: ignore
processor = ViltProcessor.from_pretrained(model_name) # type: ignore
labels = model.config.id2label # type: ignore

task = TransformersVisualQandA( # type: ignore
    predictor=TransformersModel(
        TransformersModelConfig(
            model=model
        )
    ),
    preprocess=[
        VisualQandAPreprocessor(
            VisualQandAPreprocessorConfig(
                processor=processor # type: ignore
            )
        )
    ],
    postprocess=[
        VisualQandAPostprocessor(
            VisualQandAPostprocessorConfig(
                labels=labels # type: ignore
            )
        )
    ]
)

if __name__ == "__main__":
    pipeline = (
        ImageRead()
        | AddData({"question": "How many cats are there?"})
        | task
    )

    print(Evaluator(pipeline).run_program({
        "path_to_file": "programs/program7/test.jpg"
    }))