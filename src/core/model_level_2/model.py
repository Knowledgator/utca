from abc import ABC, abstractmethod
# from typing import Any, Dict, Optional

from pydantic import BaseModel

from executable_level_1.executable import Executable
from executable_level_1.schema import InputType, OutputType

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


class ModelConfigs(BaseModel, ABC): # TODO: Check for more suitable pydantic type (no issue)
    # TODO: add basic parameters
    name: str
    
    def set_config_value(self, key: str, val: Any) -> None:
        # Optionally, add validation logic here
        self.settings[key] = val


    def get_config_value(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        # Provide a default value for missing keys
        return self.settings.get(key, default)


    def __call__(self) -> Dict[str, Any]:
        return self.settings


    def __repr__(self) -> str:
        return f"ModelConfigs({self.__str__()})"


class Model(Executable[InputType, OutputType], ABC):
    def __init__(self, cfg: ModelConfigs) -> None:
         self.cfg = cfg


    @abstractmethod
    def invoke(self, input_data: InputType) -> OutputType:
        pass


    def invoke_model(self):
        pass
