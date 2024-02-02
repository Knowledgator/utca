from abc import ABC

from core.executable_level_1.schema import InputType, OutputType
from core.model_level_2.model import Model
from core.model_level_2.schema import ConfigType

# Add abstraction, different tasks per one model
# Maybe push it inside model
class Task(Model[ConfigType, InputType, OutputType], ABC):
    ...