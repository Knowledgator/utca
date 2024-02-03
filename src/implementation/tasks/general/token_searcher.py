from typing import Any, cast, Type, Dict

from core.task_level_3.task import NERTask
from core.task_level_3.schema import (
    InputWithThreshold, 
    NEROutput,
    NERConfig 
)
from core.model_level_2.utils import (
    build_entity
)
from core.model_level_2.objects.objects import (
    Entity
)
from implementation.models.token_searcher.schema import (
    TokenSearcherModelConfig, 
    TokenSearcherModelInput, 
    TokenSearcherModelOutput
)

class TokenSearcherGeneralInput(InputWithThreshold):
    prompt: str


class TokenSearcherGeneralOutput(NEROutput[Entity]):
    prompt: str


class TokenSearcherGeneralConfig(NERConfig):
    ...


class TokenSearcherGeneralTask(
    NERTask[
        TokenSearcherGeneralConfig,
        TokenSearcherGeneralInput, 
        TokenSearcherGeneralOutput,
        TokenSearcherModelConfig, 
        TokenSearcherModelInput, 
        TokenSearcherModelOutput
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