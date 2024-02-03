from typing import Any, cast, Type, Dict, Optional

from pydantic import PrivateAttr

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

class TokenSearcherQandAInput(InputWithThreshold):
    question: str
    text: str
    _prompt: Optional[str] = PrivateAttr()

    def set_inputs(self, prompt: str) -> None:
        self._prompt = prompt


    @property
    def prompt(self) -> str:
        return cast(str, self._prompt)


class TokenSearcherQandAOutput(BaseTokenSearcherOutput[Entity]):
    prompt: str


class TokenSearcherQandAConfig(BaseTokenSearcherConfig):
    ...


class TokenSearcherQandATask(
    BaseTokenSearcher[
        TokenSearcherQandAConfig, 
        TokenSearcherQandAInput, 
        TokenSearcherQandAOutput
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