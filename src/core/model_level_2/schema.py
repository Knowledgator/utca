from __future__ import annotations
from core.executable_level_1.schema import Input

class BasicPrompt(Input):
    _prompt: str

    def __init__(self, prompt: str) -> None:
        self._prompt = prompt

    @property
    def prompt(self) -> str:
        return self._prompt


class PromptTemplate:
    def from_messages(self) -> PromptTemplate:
        return self