from typing import Any, Dict

from core.executable_level_1.actions import Action
    
class DocumentQandAPostprocess(Action[Dict[str, Any], Dict[str, Any]]):    
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return input_data["output"][0] if input_data["output"] else {"answer": "None"}