from typing import Any, Dict

from core.executable_level_1.actions import Action
from implementation.predictors.token_searcher.utils import (
    build_entity
)
from core.task_level_3.objects.objects import (
    Entity
)

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


class TokenSearcherTextCleanerPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        clean: bool=False,
        threshold: float=0.
    ) -> None:
        self.clean = clean
        self.threshold = threshold


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
            for output in input_data["output"]
            for ent in output 
            if (entity := build_entity(
                input_data["inputs"][0],
                ent, 
                self.threshold
            ))
        ]
        return {
            "text": input_data["text"],
            "output": junk,
            "cleaned_text": (
                self.clean_text(input_data["text"], junk) 
                if self.clean else None
            )
        }