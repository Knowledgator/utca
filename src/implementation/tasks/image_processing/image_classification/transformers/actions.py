from typing import Any, Dict, Protocol, Mapping, runtime_checkable

import torch

from core.executable_level_1.actions import OneToOne
from core.executable_level_1.schema import Config

@runtime_checkable
class Processor(Protocol):
    @classmethod
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        ...


class ImageClassificationPreprocessorConfig(Config):
    class Config:
        arbitrary_types_allowed = True

    processor: Processor


class ImageClassificationPreprocessor(OneToOne):
    def __init__(
        self, 
        cfg: ImageClassificationPreprocessorConfig
    ) -> None:
        self.cfg = cfg


    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self.cfg.processor(
            images=input_data["image"], 
            return_tensors="pt"
        )


class ImageClassificationPostprocessorConfig(Config):
    labels: Mapping[Any, str]
    threshold: float = 0.


class ImageClassificationSingleLabelPostprocessor(OneToOne):
    def __init__(
        self, 
        cfg: ImageClassificationPostprocessorConfig
    ) -> None:
        self.cfg = cfg


    def execute(
        self, input_data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        predicted_class_idx = input_data["outputs"]["logits"].argmax(-1).item()
        return {
            "label": self.cfg.labels[predicted_class_idx]
        }


class ImageClassificationMultyLabelPostprocessor(OneToOne):
    def __init__(
        self, 
        cfg: ImageClassificationPostprocessorConfig
    ) -> None:
        self.cfg = cfg


    def execute(
        self, input_data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        probabilities = torch.nn.functional.softmax(
            input_data["outputs"]["logits"], dim=-1
        )
        probabilities = probabilities.detach().numpy().tolist()[0]

        return {
            "labels": {
                self.cfg.labels[i]: prob for i, prob in enumerate(probabilities)
            }
        }