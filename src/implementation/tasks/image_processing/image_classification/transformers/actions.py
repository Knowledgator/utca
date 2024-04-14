from typing import Any, Dict, Protocol, Mapping, runtime_checkable

import torch

from core.executable_level_1.actions import Action

@runtime_checkable
class Processor(Protocol):
    @classmethod
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        ...


class ImageClassificationPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        processor: Processor
    ) -> None:
        self.processor = processor


    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            "pixel_values": self.processor(
                images=input_data["image"], 
                return_tensors="pt"
            )["pixel_values"]
        }


class ImageClassificationSingleLabelPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        labels: Mapping[Any, str],
        threshold: float = 0.
    ) -> None:
        self.labels = labels
        self.threshold = threshold


    def execute(
        self, input_data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        predicted_class_idx = input_data["logits"].argmax(-1).item()
        return {
            "label": self.labels[predicted_class_idx]
        }


class ImageClassificationMultilabelPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        labels: Mapping[Any, str],
        threshold: float = 0.
    ) -> None:
        self.labels = labels
        self.threshold = threshold


    def execute(
        self, input_data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        probabilities = torch.nn.functional.softmax(
            input_data["logits"], dim=-1
        )
        probabilities = probabilities.detach().numpy().tolist()[0]

        return {
            "labels": {
                self.labels[i]: prob 
                for i, prob in enumerate(probabilities)
                if prob >= self.threshold
            }
        }