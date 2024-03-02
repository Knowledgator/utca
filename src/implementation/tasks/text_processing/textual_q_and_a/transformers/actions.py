from typing import Any, Dict, Optional

from core.executable_level_1.schema import Config
from core.executable_level_1.actions import OneToOne

class QandAPostprocessorConfig(Config):
    threshold: float = 0.


class QandAPostprocess(OneToOne):
    def __init__(
        self, 
        cfg: Optional[QandAPostprocessorConfig]=None
    ) -> None:
        self.cfg = cfg or QandAPostprocessorConfig()
    
    
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            "answer": input_data["outputs"]["answer"]
        }