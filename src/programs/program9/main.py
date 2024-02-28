from core.executable_level_1.schema import Transformable
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig
)
from implementation.tasks.summarization.transformers_summarization import (
    SummarizationTask
)

model_name = "facebook/bart-large-cnn"

predictor = TransformersPipeline(
    TransformersPipelineConfig(
        task="summarization", 
        model=model_name
    )
)

task = SummarizationTask(
    predictor=predictor,
)

if __name__ == "__main__":
    with open("programs/program9/text.txt", "r") as f:
        text = f.read()
    print(task.execute(Transformable({
        "inputs": {
            "inputs": text,
            "max_length": 200,
            "min_length": 100
        }
    })).extract())