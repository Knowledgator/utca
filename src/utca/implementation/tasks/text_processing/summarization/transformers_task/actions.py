from typing import Any, Dict

from utca.core.executable_level_1.actions import Action
    
class SummarizationPostprocess(Action[Dict[str, Any], Dict[str, Any]]):    
    """
    Format model output

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "output" (Any): Model output;
    
    Returns:
        Dict[str, Any]: Expected keys:
            "summary_text" (str);
    """
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "output" (Any): Model output;
        
        Returns:
            Dict[str, Any]: Expected keys:
                "summary_text" (str);
        """
        return input_data["output"][0]