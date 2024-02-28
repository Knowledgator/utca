from core.executable_level_1.schema import Transformable
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig
)
from implementation.tasks.textual_q_and_a.transformers_q_and_a import (
    QandATask
)

model_name = "deepset/roberta-base-squad2"

predictor = TransformersPipeline(
    TransformersPipelineConfig(
        task="question-answering", 
        model=model_name
    )
)

task = QandATask(
    predictor=predictor,
)

if __name__ == "__main__":
    print(task.execute(Transformable({
        "question": "Hwo is a president of USA?",
        "context": "Joseph Robinette Biden Jr. is an American politician who is the 46th and current president of the United States."
    })).extract())