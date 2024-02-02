from typing import Any, Union, cast, Type, Dict, Optional

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
    input_data_type: Type[TokenSearcherQandAInput] = TokenSearcherQandAInput
    prompt: str = """{question}
Text:
 """
    def _preprocess(
        self, input_data: Union[TokenSearcherQandAInput, Dict[str, Any]]
    ) -> TokenSearcherQandAInput:
        input_data = super()._preprocess(input_data)
        input_data.set_inputs(
            self.prompt.format(question=input_data.question) + input_data.text
        )
        return input_data


    def _process(
        self, input_data: TokenSearcherQandAInput
    ) -> list[list[Dict[str, Any]]]:
        return self.get_predictions([input_data.prompt])
    

    def _postprocess(
        self, 
        input_data: TokenSearcherQandAInput, 
        predicts: list[list[Dict[str, Any]]]
    ) -> TokenSearcherQandAOutput:
        return TokenSearcherQandAOutput(
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