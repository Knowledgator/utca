from typing import Dict, Any, Generic
from abc import abstractmethod

from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import (
    InputType, OutputType, ConfigType
)
from core.model_level_2.model import Model
from core.model_level_2.schema import ModelConfigType, ModelInputType, ModelOutputType

class Task(
    Executable[ConfigType, InputType, OutputType],
    Generic[
        ConfigType, InputType, OutputType,
        ModelConfigType, ModelInputType, ModelOutputType
    ]
):
    def __init__(
        self, cfg: ConfigType, model: Model[ModelConfigType, ModelInputType, ModelOutputType] 
    ) -> None:
        super().__init__(cfg)
        self.model = model


    @abstractmethod
    def _preprocess(
        self, input_data: InputType
    ) -> InputType:
        ...


    @abstractmethod
    def _postprocess(
        self, 
        input_data: InputType, 
        output_data: Any
    ) -> Dict[str, Any]:
        ...
