from core.executable_level_1.schema import Transformable
# from core.executable_level_1.interpreter import Evaluator
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig
)
from implementation.tasks.token_classification.transformers_token_classification import (
    TokenClassifierTask
)

model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"

predictor = TransformersPipeline(
    TransformersPipelineConfig(
        task="token-classification", 
        model=model_name
    )
)

task = TokenClassifierTask(
    predictor=predictor
)

if __name__ == "__main__":
    print(task.execute(Transformable({
        "inputs": "My name is Sarah and I live in London"
    })).extract())
    # pipeline = predictor

    # print(Evaluator(pipeline).run_program({
    #     "path_to_file": "programs/program7/test.jpg"
    # }))