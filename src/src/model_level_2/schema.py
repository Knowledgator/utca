from __future__ import annotations
# from src.executable_level_1.schema import InputType

class Prompt:
    def __init__(self, prompt: str) -> None:
        self._prompt = prompt


    @property
    def prompt(self) -> str:
        return self._prompt


class PromptTemplate:
    def from_messages(self) -> PromptTemplate:
        return self