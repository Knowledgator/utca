from typing import Generic, Type, Any, Union, Dict
from abc import ABC, abstractmethod

from core.executable_level_1.schema import InputType, OutputType
from core.model_level_2.schema import ConfigType


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

class Model(Generic[ConfigType, InputType, OutputType], ABC):
    input_data_type: Type[InputType]

    def __init__(self, cfg: ConfigType):
        self.cfg: ConfigType = cfg


    @abstractmethod
    def get_predictions(
        self, inputs: Any
    ) -> Any:
        ...


    @abstractmethod
    def _preprocess(
        self, input_data: Union[InputType, Dict[str, Any]]
    ) -> InputType:
        ...


    @abstractmethod
    def _process(
        self, input_data: InputType
    ) -> Any:
        ...


    @abstractmethod
    def _postprocess(
        self, 
        input_data: InputType, 
        predicts: Any
    ) -> OutputType:
        ...


    @abstractmethod
    def execute(
        self, 
        input_data: Union[InputType, Dict[str, Any]]
    ) -> OutputType:
        ...
