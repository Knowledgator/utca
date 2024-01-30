from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, TypeVar

from src import executable_level_1
from src.executable_level_1.executable import Executable, IOValidator


class ModelIOValidator(IOValidator, ABC):
        
    @abstractmethod
    def isValidInput(self, input_data: Input) -> bool:
        pass
    @abstractmethod
    def isValidOutput(self, output_data: Output) -> bool:
        pass




# class ModelInput(Input):
#     def __init__(self, value: Optional[Dict[Any, Any]] = None) -> None: 
#         self.value = value if value is not None else {}
#     value: Dict[Any, Any]

# class ModelOutput(Output):
#     pass



class ModelConfigs:
    def __init__(self, settings: Optional[Dict[str, Any]] = None) -> None:
        # Initialize with default settings
        # TODO
        self.settings: dict[str, str] = {"default_key": "default_value"}
        if settings:
            self.settings.update(settings)

    def set_config_value(self, key: str, val: Any) -> None:
        # Optionally, add validation logic here
        self.settings[key] = val

    def get_config_value(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        # Provide a default value for missing keys
        return self.settings.get(key, default)

    def __call__(self) -> Dict[str, Any]:
        return self.settings

    def __repr__(self) -> str:
        return f"ModelConfigs({self.settings})"


class Model(Executable, ABC):
    def __init__(self, cfg: ModelConfigs) -> None:
         self.cfg = cfg
    def invoke(self):
        pass
    def invoke_model():
        pass
