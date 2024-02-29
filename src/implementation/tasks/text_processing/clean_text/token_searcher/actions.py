from typing import Any, Dict, Optional

from core.executable_level_1.actions import Action, OneToOne
from core.executable_level_1.schema import Config
from core.task_level_3.utils import (
    build_entity
)
from core.task_level_3.objects.objects import (
    Entity
)

@OneToOne
class TokenSeatcherTextCleanerPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    prompt: str = """
Clean the following text extracted from the web matching not relevant parts:

{text}
"""

    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        input_data["inputs"] = [self.prompt.format(text=input_data["text"])]
        return input_data


class TokenSearcherTextCleanerPostprocessorConfig(Config):
    clean: bool = False
    threshold: float = 0.


@OneToOne
class TokenSearcherTextCleanerPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        cfg: Optional[TokenSearcherTextCleanerPostprocessorConfig] = None
    ) -> None:
        self.cfg = cfg or TokenSearcherTextCleanerPostprocessorConfig()


    @classmethod
    def clean_text(cls, text: str, junk: list[Entity]) -> str:
        clean = ""
        start = 0
        for ent in junk:
            clean += text[start:ent.start].strip() + " "
            start = ent.end
        clean += text[start:].strip()
        return clean


    def execute(
        self, input_data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        junk = [
            entity
            for output in input_data["outputs"]
            for ent in output 
            if (entity := build_entity(
                input_data["inputs"]["inputs"][0],
                ent, 
                self.cfg.threshold
            ))
        ]
        return {
            "text": input_data["inputs"]["text"],
            "output": junk,
            "cleaned_text": (
                self.clean_text(input_data["inputs"]["text"], junk) 
                if self.cfg.clean else None
            )
        }