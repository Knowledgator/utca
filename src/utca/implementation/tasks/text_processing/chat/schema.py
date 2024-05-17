from typing import Generator

from utca.core.executable_level_1.schema import IOModel

class ChatInput(IOModel):
    prompt: str


class ChatOutput(IOModel):
    message: str


class ChatStreamOutput(IOModel):
    stream: Generator[str, None, None]