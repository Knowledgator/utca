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

class TokenSearcherTextCleanerInput(InputWithThreshold):
    text: str
    clean: Optional[bool] = None
    _prompt: Optional[str] = PrivateAttr()

    def set_inputs(self, prompt: str) -> None:
        self._prompt = prompt


    @property
    def prompt(self) -> str:
        return cast(str, self._prompt)


class TokenSearcherTextCleanerOutput(BaseTokenSearcherOutput[Entity]):
    text: str
    cleaned_text: Optional[str] = None


class TokenSearcherTextCleanerConfig(BaseTokenSearcherConfig):
    clean: bool = False


class TokenSearcherTextCleanerTask(
    BaseTokenSearcher[
        TokenSearcherTextCleanerConfig,
        TokenSearcherTextCleanerInput, 
        TokenSearcherTextCleanerOutput
    ]
):
    input_class: Type[TokenSearcherTextCleanerInput] = TokenSearcherTextCleanerInput
    output_class: Type[TokenSearcherTextCleanerOutput] = TokenSearcherTextCleanerOutput
    prompt: str = """
Clean the following text extracted from the web matching not relevant parts:

{text}
"""

    def _preprocess(
        self, input_data: TokenSearcherTextCleanerInput
    ) -> TokenSearcherTextCleanerInput:
        input_data = super()._preprocess(input_data)
        input_data.set_inputs(
            self.prompt.format(text=input_data.text)
        )
        input_data.clean = (
            input_data.clean if isinstance(input_data.clean, bool) else self.cfg.clean
        )
        return input_data


    def invoke(
        self, input_data: TokenSearcherTextCleanerInput
    ) -> Dict[str, Any]:
        self._preprocess(input_data)
        predcits = self.model.execute(
            {'inputs': [input_data.prompt]}, Dict[str, Any]
        )
        return self._postprocess(input_data, predcits)


    @classmethod
    def clean_text(cls, text: str, junk: list[Entity]) -> str:
        clean = ''
        start = 0
        for ent in junk:
            clean += text[start:ent.start].strip() + ' '
            start = ent.end
        clean += text[start:].strip()
        return clean


    def _postprocess(
        self, 
        input_data: TokenSearcherTextCleanerInput, 
        output_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        junk = [
            entity
            for output in output_data['outputs']
            for ent in output 
            if (entity := build_entity(
                input_data.prompt, ent, cast(float, input_data.threshold)
            ))
        ]
        return {
            'text': input_data.text,
            'output': junk,
            'cleaned_text': (
                self.clean_text(input_data.text, junk) 
                if input_data.clean else None
            )
        }