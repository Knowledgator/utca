from typing import Any, Dict

from core.executable_level_1.actions import Action
from implementation.predictors.token_searcher.utils import (
    build_entity
)

class TokenSearcherQandAPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    prompt: str = """{question}
Text:
 """
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        input_data["inputs"] = [
            self.prompt.format(question=input_data["question"]) 
            + input_data["text"]
        ]
        return input_data
    

class TokenSearcherQandAPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        threshold: float = 0.
    ) -> None:
        self.threshold = threshold
    
    
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            'text': input_data["text"],
            'question': input_data["question"],
            'output': [
                entity
                for output in input_data["output"]
                for ent in output 
                if (entity := build_entity(
                    input_data["inputs"][0],
                    ent,
                    self.threshold
                ))
            ]
        }