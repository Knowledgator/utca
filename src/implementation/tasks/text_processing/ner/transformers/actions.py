from typing import Any, Dict, Optional

from core.executable_level_1.actions import Action
    
class TokenClassifierPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        threshold: float=0.,
        name: Optional[str]=None,
    ) -> None:
        super().__init__(name)
        self.threshold = threshold
    
    
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