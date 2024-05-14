from typing import Union
import re

from utca.core.executable_level_1.interpreter import Evaluator
from utca.core.executable_level_1.schema import Transformable

class RePattern:
    """
    Regular expression conditions 
    """
    def __init__(
        self, 
        pattern: Union[re.Pattern[str], str],
        get_key: str
    ) -> None:
        """
        Args:
            pattern (Union[re.Pattern[str], str]): Regular expression pattern.
            
            get_key (str): Key associated with data of type str that will be checked.
        """
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        self.pattern = pattern
        self.get_key = get_key


    def search(self, input_data: Transformable, evaluator: Evaluator) -> bool:
        return bool(self.pattern.search(getattr(input_data, self.get_key)))
    

    def match(self, input_data: Transformable, evaluator: Evaluator) -> bool:
        return bool(self.pattern.match(getattr(input_data, self.get_key)))