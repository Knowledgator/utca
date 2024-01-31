from typing import Dict, Any

from implementation.models.token_searcher.model import TokenSearcher
from core.executable_level_1.schema import Input, Output
from core.task_level_3.task import Task

class TokenSearcherNERInput(Input):
    pass


class TokenSearcherNEROutput(Output):
    pass


class TokenSearcherNERTask(Task[TokenSearcherNERInput, TokenSearcherNEROutput]):
    pass