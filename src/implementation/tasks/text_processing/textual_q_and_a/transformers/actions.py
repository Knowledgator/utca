from typing import Any, Dict, Optional

from core.executable_level_1.schema import Config
from core.executable_level_1.actions import Action

class QandAPostprocessorConfig(Config):
    threshold: float = 0.


class QandAPostprocess(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        cfg: Optional[QandAPostprocessorConfig]=None
    ) -> None:
        self.cfg = cfg or QandAPostprocessorConfig()
    
    
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return (
            input_data 
            if input_data["score"] > self.cfg.threshold 
            else {}
        )