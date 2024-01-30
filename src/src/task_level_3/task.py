from abc import ABC

from src.model_level_2.model import Model

# Add abstraction, different tasks per one model
# Maybe push it inside model
class Task(Model, ABC):
    def __init__(self, model: Model, taskName: str) -> None:
        self.taks = taskName
        self.model = model
    prompt: str
    prompt_len: int
    def preprocess(self):
        # add prompt
        pass

    def postprocess(self):
        pass
    def process(self):
        self.preprocess()
        self.invoke()
        self.postprocess()