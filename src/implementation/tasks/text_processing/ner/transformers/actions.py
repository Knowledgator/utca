from typing import Any, Dict, Optional

from core.executable_level_1.schema import Config
from core.executable_level_1.actions import Action
    
class TokenClassifierPostprocessorConfig(Config):
    threshold: float = 0.


class TokenClassifierPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        cfg: Optional[TokenClassifierPostprocessorConfig]=None
    ) -> None:
        self.cfg = cfg or TokenClassifierPostprocessorConfig()
    
    
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            'output': [
                {
                    **output,
                    "span": output["word"]
                }
                for output in input_data["output"]
            ]
        }