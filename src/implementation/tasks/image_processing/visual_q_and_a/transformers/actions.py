from typing import Any, Dict, Mapping, Optional, Protocol, runtime_checkable

import torch

from core.executable_level_1.actions import Action

@runtime_checkable
class Processor(Protocol):
    @classmethod
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        ...


class VisualQandAPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        processor: Processor,
        name: Optional[str]=None,
    ) -> None:
        super().__init__(name)
        self.processor = processor


    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self.processor(
            images=input_data["image"],
            text=input_data["question"],
            return_tensors="pt"
        ).data


class VisualQandAMultianswerPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        labels: Mapping[Any, str],
        threshold: float = 0.,
        name: Optional[str]=None,
    ) -> None:
        super().__init__(name)
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
            "answers": {
                self.labels[i]: prob 
                for i, prob in enumerate(probabilities)
                if prob >= self.threshold
            }
        }


class VisualQandASingleAnswerPostprocessor(
    VisualQandAMultianswerPostprocessor
):
    def execute(
        self, input_data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        answers = super().execute(input_data)['answers']
        sorted_answers = sorted(answers.items(), key=(lambda a: a[1]), reverse=True)
        return {
            "answer": sorted_answers[0] if sorted_answers else None
        }