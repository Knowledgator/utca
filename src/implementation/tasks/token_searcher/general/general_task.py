from typing import Any, cast, Type, Dict

from implementation.tasks.token_searcher.base_token_searcher_task.base_token_searcher import (
    BaseTokenSearcher, 
    InputWithThreshold, 
    BaseTokenSearcherOutput, 
    BaseTokenSearcherConfig
)
from implementation.tasks.token_searcher.base_token_searcher_task.utils import (
    build_entity
)
from implementation.tasks.token_searcher.base_token_searcher_task.objects import (
    Entity
)

class TokenSearcherGeneralInput(InputWithThreshold):
    prompt: str


class TokenSearcherGeneralOutput(BaseTokenSearcherOutput[Entity]):
    prompt: str


class TokenSearcherGeneralConfig(BaseTokenSearcherConfig):
    ...


class TokenSearcherGeneralTask(
    BaseTokenSearcher[TokenSearcherGeneralInput, TokenSearcherGeneralOutput]
):
    input_data_type: Type[TokenSearcherGeneralInput] = TokenSearcherGeneralInput
    
    def _process(
        self, input_data: TokenSearcherGeneralInput
    ) -> list[list[Dict[str, Any]]]:
        return self.get_predictions([input_data.prompt])
    

    def _postprocess(
        self, 
        input_data: TokenSearcherGeneralInput, 
        predicts: list[list[Dict[str, Any]]]
    ) -> TokenSearcherGeneralOutput:
        return TokenSearcherGeneralOutput(
            prompt=input_data.prompt,
            output=[
                entity
                for output in predicts
                for ent in output 
                if (entity := build_entity(
                    input_data.prompt, ent, cast(float, input_data.threshold)
                ))
            ]
        )