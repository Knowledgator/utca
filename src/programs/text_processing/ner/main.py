from core.executable_level_1.schema import Transformable
# from core.executable_level_1.interpreter import Evaluator
from implementation.tasks.text_processing.ner.transformers.transformers_token_classification import (
    TokenClassifierTask
)

task = TokenClassifierTask()

if __name__ == "__main__":
    print(task.execute(Transformable({
        "inputs": "My name is Sarah and I live in London"
    })).extract())
    # pipeline = predictor

    # print(Evaluator(pipeline).run_program({
    #     "path_to_file": "programs/program7/test.jpg"
    # }))