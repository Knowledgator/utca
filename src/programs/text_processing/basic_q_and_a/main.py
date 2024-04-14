from core.executable_level_1.schema import Transformable
from implementation.tasks.text_processing.textual_q_and_a.transformers.transformers_q_and_a import (
    TransformersTextualQandA
)

task = TransformersTextualQandA()

if __name__ == "__main__":
    print(task(Transformable({
        "question": "Hwo is a president of USA?",
        "context": "Joseph Robinette Biden Jr. is an American politician who is the 46th and current president of the United States."
    })).extract())