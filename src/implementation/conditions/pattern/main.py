from typing import Union
import re

from core.executable_level_1.schema import Transformable
# query / subject

class RePattern:
    def __init__(
        self, 
        pattern: Union[re.Pattern[str], str],
        key: str
    ) -> None:
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        self.pattern = pattern
        self.key = key


    def search(self, input_data: Transformable) -> bool:
        return bool(self.pattern.search(getattr(input_data, self.key)))
    

    def match(self, input_data: Transformable) -> bool:
        return bool(self.pattern.match(getattr(input_data, self.key)))