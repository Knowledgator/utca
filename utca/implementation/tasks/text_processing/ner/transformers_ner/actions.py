from typing import Any, Dict, Optional

from utca.core.executable_level_1.actions import Action
    
class TokenClassifierPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Format model output
    
    Args:
        input_data (Dict[str, Any]): Expected keys:
            "output" (List[Dict[str, Any]]): Model output;

    Returns:
        Dict[str, Any]: Expected keys:
            "output" (List[ClassifiedEntity]): Classified entities;
    """
    def __init__(
        self, 
        threshold: float=0.,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            threshold (float): Entities threshold score. Defaults to 0.

            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.threshold = threshold
    
    
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "output" (List[Dict[str, Any]]): Model output;

        Returns:
            Dict[str, Any]: Expected keys:
                "output" (List[ClassifiedEntity]): Classified entities;
        """
        return {
            'output': [
                {
                    **output,
                    "span": output["word"]
                }
                for output in input_data["output"]
            ]
        }