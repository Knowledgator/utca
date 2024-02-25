from abc import ABC, abstractmethod
from typing import Any

# implement visualizer with i/o actions (updated writer)

class Visualizer(ABC):
    doc: Any
    @abstractmethod
    def draw(self):
        pass

class VideoVis(Visualizer):
    pass

class ImgVis(Visualizer):
    pass


class TextWordVis(Visualizer):
    pass