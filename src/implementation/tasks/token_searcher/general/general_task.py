from typing import Dict, Any

from implementation.models.token_searcher.model import TokenSearcher
from core.executable_level_1.schema import Output
from core.model_level_2.schema import BasicPrompt, PromptTemplate
from core.task_level_3.task import Task

# class TokenSearcherNERInput(Input):
#     pass


class TokenSearcherGeneralOutput(Output):
    pass


class TokenSearcherGeneralTask(Task[BasicPrompt, TokenSearcherGeneralOutput]):
    model_type = TokenSearcher
    template = PromptTemplate('{prompt}')

    def preprocess(self, input_data: BasicPrompt) -> BasicPrompt:
        return input_data
    

    def postprocess(self, output_data: Dict[str, Any]) -> Dict[str, Any]:
        return output_data