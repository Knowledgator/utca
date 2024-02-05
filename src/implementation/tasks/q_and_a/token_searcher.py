from typing import Any, cast, Type, Dict, Optional

from pydantic import PrivateAttr

from core.task_level_3.task import NERTask
from core.task_level_3.schema import (
    InputWithThreshold, 
    NEROutput,
    NERConfig 
)
from core.task_level_3.utils import (
    build_entity
)
from core.task_level_3.objects.objects import (
    Entity
)
from implementation.models.token_searcher.schema import (
    TokenSearcherModelConfig, 
    TokenSearcherModelInput, 
    TokenSearcherModelOutput
)

class TokenSearcherQandAInput(InputWithThreshold):
    question: str
    text: str
    _prompt: Optional[str] = PrivateAttr()

    def set_inputs(self, prompt: str) -> None:
        self._prompt = prompt


    @property
    def prompt(self) -> str:
        return cast(str, self._prompt)


class TokenSearcherQandAOutput(NEROutput[Entity]):
    prompt: str


class TokenSearcherQandAConfig(NERConfig):
    ...


class TokenSearcherQandATask(
    NERTask[
        TokenSearcherQandAConfig, 
        TokenSearcherQandAInput, 
        TokenSearcherQandAOutput,
        TokenSearcherModelConfig, 
        TokenSearcherModelInput, 
        TokenSearcherModelOutput
    ]
):
    input_class: Type[TokenSearcherQandAInput] = TokenSearcherQandAInput
    output_class: Type[TokenSearcherQandAOutput] = TokenSearcherQandAOutput

    prompt: str = """{question}
Text:
 """
    def _preprocess(
        self, input_data: TokenSearcherQandAInput
    ) -> TokenSearcherQandAInput:
        input_data = super()._preprocess(input_data)
        input_data.set_inputs(
            self.prompt.format(question=input_data.question) + input_data.text
        )
        return input_data


    def invoke(
        self, input_data: TokenSearcherQandAInput
    ) -> Dict[str, Any]:
        input_data = self._preprocess(input_data)
        predicts = self.model.execute(
            {'inputs': [input_data.prompt]}, Dict[str, Any]
        )
        return self._postprocess(input_data, predicts)
    

    def invoke_batch(
        self, input_data: list[TokenSearcherQandAInput]
    ) -> list[Dict[str, Any]]:
        raise Exception('TODO!')


    def _postprocess(
        self, 
        input_data: TokenSearcherQandAInput, 
        output_data: Dict[str, Any]
    ) -> Dict[str, Any]:
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