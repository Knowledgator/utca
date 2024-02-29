from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.actions import (
    AddData
)
from implementation.tasks.image_processing.visual_q_and_a.transformers.transformers_visual_q_and_a import (
    TransformersVisualQandA
)
from implementation.datasources.image.actions import ImageRead

task = TransformersVisualQandA()

if __name__ == "__main__":
    pipeline = (
        ImageRead()
        | AddData({"question": "How many cats are there?"})
        | task
    )

    print(Evaluator(pipeline).run_program({
        "path_to_file": "programs/image_processing/visual_q_and_a/test.jpg"
    }))