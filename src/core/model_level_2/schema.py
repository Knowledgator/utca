from __future__ import annotations
from core.executable_level_1.schema import Input

class BasicPrompt(Input):
    prompt: str


class PromptTemplate:
    def from_messages(self) -> PromptTemplate:
        return self