from typing import Any, cast, Type, Dict

from implementation.tasks.token_searcher.base_token_searcher_task.base_token_searcher import (
    BaseTokenSearcher
)
from implementation.tasks.token_searcher.base_token_searcher_task.schema import (
    InputWithThreshold, 
    BaseTokenSearcherOutput, 
    BaseTokenSearcherConfig
)
from implementation.tasks.token_searcher.base_token_searcher_task.utils import (
    build_entity
)
from implementation.models.objects.objects import (
    Entity
)

class TokenSearcherGeneralInput(InputWithThreshold):
    prompt: str


class TokenSearcherGeneralOutput(BaseTokenSearcherOutput[Entity]):
    prompt: str


class TokenSearcherGeneralConfig(BaseTokenSearcherConfig):
    ...


class TokenSearcherGeneralTask(
    BaseTokenSearcher[
        TokenSearcherGeneralConfig,
        TokenSearcherGeneralInput, 
        TokenSearcherGeneralOutput
    ]
):
    input_class: Type[TokenSearcherGeneralInput] = TokenSearcherGeneralInput
    output_class: Type[TokenSearcherGeneralOutput] = TokenSearcherGeneralOutput

    def invoke(
        self, input_data: TokenSearcherGeneralInput
    ) -> Dict[str, Any]:
        input_data = self._preprocess(input_data)
        predicts = self.model.execute({'inputs':[input_data.prompt]}, return_type=Dict[str, Any])
        return self._postprocess(input_data, predicts)


    def _postprocess(
        self, 
        input_data: TokenSearcherGeneralInput, 
        output_data: Dict[str, Any]
    ) ->  Dict[str, Any]:
        return {
            'prompt': input_data.prompt,
            'output': [
                entity
                for output in output_data['outputs']
                for ent in output 
                if (entity := build_entity(
                    input_data.prompt, ent, cast(float, input_data.threshold)
                ))
            ]
        }