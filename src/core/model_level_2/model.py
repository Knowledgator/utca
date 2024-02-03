from core.executable_level_1.executable import Executable
from core.model_level_2.schema import (
    ModelInputType,
    ModelOutputType,
    ModelConfigType
)


# class ModelInput(Input):
#     def __init__(self, value: Optional[Dict[Any, Any]] = None) -> None: 
#         self.value = value if value is not None else {}
#     value: Dict[Any, Any]

# class ModelOutput(Output):
#     pass


# class ModelConfigs(BaseModel, ABC): # TODO: Check for more suitable pydantic type (no issue)
#     # TODO: add basic parameters
    
#     # def set_config_value(self, key: str, val: Any) -> None:
#     #     # Optionally, add validation logic here
#     #     self.settings[key] = val
    
#     # def set_config_value(self, key: str, val: Any) -> None:
#     #     # Optionally, add validation logic here
#     #     self.settings[key] = val


#     # def get_config_value(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
#     #     # Provide a default value for missing keys
#     #     return self.settings.get(key, default)
#     # def get_config_value(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
#     #     # Provide a default value for missing keys
#     #     return self.settings.get(key, default)


#     # def __call__(self) -> Dict[str, Any]:
#     #     return self.settings
#     # def __call__(self) -> Dict[str, Any]:
#     #     return self.settings

# class Model(Generic[InputType], ABC):
#     def __init__(self, cfg: ModelConfigs) -> None:
#         self.cfg = cfg


#     @abstractmethod
#     def invoke(self, input_data: InputType) -> OutputType:
#         pass


#     # def invoke_model(self):
#     #     pass


class Model(Executable[ModelConfigType, ModelInputType, ModelOutputType]):
    ...