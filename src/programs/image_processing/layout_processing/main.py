from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.actions import (
    AddData
)
from implementation.tasks.image_processing.documents_q_and_a.transformers.transformers_layout_lm import (
    DocumentQandATask
)
from implementation.datasources.image.actions import ImageRead

task = DocumentQandATask()

if __name__ == "__main__":
    pipeline = (
        ImageRead()
        | AddData({
            "question": "What is the purchase amount?"
        })
        | task
    )

    print(Evaluator(pipeline).run_program({
        "path_to_file": "programs/image_processing/layout_processing/test.jpeg"
    }))