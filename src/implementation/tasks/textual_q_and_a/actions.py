from typing import Any, Dict, Optional

from core.executable_level_1.schema import Config
from core.executable_level_1.actions import Action, OneToOne
from core.task_level_3.utils import (
    build_entity
)

@OneToOne
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
    

class TokenSearcherQandAPostprocessorConfig(Config):
    threshold: float = 0.


@OneToOne
class TokenSearcherQandAPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        cfg: Optional[TokenSearcherQandAPostprocessorConfig]=None
    ) -> None:
        self.cfg = cfg or TokenSearcherQandAPostprocessorConfig()
    
    
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            'text': input_data["inputs"]["text"],
            'question': input_data["inputs"]["question"],
            'output': [
                entity
                for output in input_data["outputs"]
                for ent in output 
                if (entity := build_entity(
                    input_data["inputs"]["inputs"][0],
                    ent,
                    self.cfg.threshold
                ))
            ]
        }