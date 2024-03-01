from typing import Any, Dict

from core.executable_level_1.actions import Action, OneToOne
    

@OneToOne
class DocumentQandAPostprocess(
    Action[Dict[str, Any], Dict[str, Any]]
):    
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return input_data["outputs"][0]