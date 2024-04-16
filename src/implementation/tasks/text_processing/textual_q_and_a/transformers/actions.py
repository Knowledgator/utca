from typing import Any, Dict, Optional

from core.executable_level_1.actions import Action

class QandAPostprocess(Action[Dict[str, Any], Dict[str, Any]]):
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
        return (
            input_data 
            if input_data["score"] > self.threshold 
            else {}
        )