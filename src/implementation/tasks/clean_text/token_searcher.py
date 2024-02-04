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

class TokenSearcherTextCleanerInput(InputWithThreshold):
    text: str
    clean: Optional[bool] = None
    _prompt: Optional[str] = PrivateAttr()

    def set_inputs(self, prompt: str) -> None:
        self._prompt = prompt


    @property
    def prompt(self) -> str:
        return cast(str, self._prompt)


class TokenSearcherTextCleanerOutput(NEROutput[Entity]):
    text: str
    cleaned_text: Optional[str] = None


class TokenSearcherTextCleanerConfig(NERConfig):
    clean: bool = False


class TokenSearcherTextCleanerTask(
    NERTask[
        TokenSearcherTextCleanerConfig,
        TokenSearcherTextCleanerInput, 
        TokenSearcherTextCleanerOutput,
        TokenSearcherModelConfig, 
        TokenSearcherModelInput, 
        TokenSearcherModelOutput
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