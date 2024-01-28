from abc import ABC

from src.model import Model

# Add abstraction, different tasks per one model
# Maybe push it inside model
class Task(ABC):
    def __init__(self, model: Model, taskName: str) -> None:
        self.taks = taskName
        self.model = model