from utca.implementation.tasks.text_processing.textual_q_and_a.transformers_task.transformers_q_and_a import (
    TransformersTextualQandA
)

task = TransformersTextualQandA()

if __name__ == "__main__":
    print(task.run({
        "question": "Hwo is a president of USA?",
        "context": "Joseph Robinette Biden Jr. is an American politician who is the 46th and current president of the United States."
    }))