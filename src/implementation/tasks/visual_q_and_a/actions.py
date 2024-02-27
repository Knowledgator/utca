from typing import Any, Dict, Protocol, Mapping, runtime_checkable

from core.executable_level_1.actions import Action, OneToOne
from core.executable_level_1.schema import Config

@runtime_checkable
class Processor(Protocol):
    @classmethod
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        ...


class VisualQandAPreprocessorConfig(Config):
    class Config:
        arbitrary_types_allowed = True

    processor: Processor


@OneToOne
class VisualQandAPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        cfg: VisualQandAPreprocessorConfig
    ) -> None:
        self.cfg = cfg


    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        input_data["inputs"] = self.cfg.processor(
            images=input_data["image"],
            text=input_data["question"],
            return_tensors="pt"
        )
        return input_data


class VisualQandAPostprocessorConfig(Config):
    labels: Mapping[Any, str]
    threshold: float = 0.


@OneToOne
class VisualQandAPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        cfg: VisualQandAPostprocessorConfig
    ) -> None:
        self.cfg = cfg


    def execute(
        self, input_data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        predicted_class_idx = input_data["outputs"]["logits"].argmax(-1).item()
        return {
            "outputs": {"answer": self.cfg.labels[predicted_class_idx]}
        }