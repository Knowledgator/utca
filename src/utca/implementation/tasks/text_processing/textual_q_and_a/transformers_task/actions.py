from typing import Any, Dict, Optional

from utca.core.executable_level_1.actions import Action

class QandAPostprocess(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Check if answer score is higher than threshold
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
        Arguments:
            input_data (Dict[str, Any]): Expected keys:
                "answer" (Optional[str], optional);

                "score" (float);
        Returns:
            Dict[str, Any]: Expected keys:
                "answer" (Optional[str], optional);
                
                "score" (float);
        """
        return (
            input_data 
            if input_data["score"] > self.threshold 
            else {}
        )