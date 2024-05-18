from typing import Any, Dict, Optional, Protocol, Mapping, runtime_checkable

import torch

from utca.core.executable_level_1.actions import Action

@runtime_checkable
class Processor(Protocol):
    @classmethod
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        ...


class ImageClassificationPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Prepare model input
    """
    def __init__(
        self, 
        processor: Processor,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            processor (Processor): Feature extractor.
            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.processor = processor


    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "image" (Image.Image): Image to analyze;
        Returns:
            Dict[str, Any]: Expected keys:
                "pixel_values" (Any);
        """
        return self.processor(
            images=input_data["image"], 
            return_tensors="pt"
        ).data


class ImageClassificationMultilabelPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Process model output
    """
    def __init__(
        self, 
        labels: Mapping[Any, str],
        threshold: float = 0.,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            labels (Mapping[Any, str]): Labels for classification.
            
            threshold (float): Labels threshold score. Defaults to 0.
            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.labels = labels
        self.threshold = threshold


    def execute(
        self, input_data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "logits" (Any): Model output;
        
        Returns:
            Dict[str, Any]: Expected keys:
                "labels" (Dict[str, float]): Classified labels and scores.
        """
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
    

class ImageClassificationSingleLabelPostprocessor(
    ImageClassificationMultilabelPostprocessor
):
    def execute(
        self, input_data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        """
        Arguments:
            input_data (Dict[str, Any]): Expected keys:
                "logits" (Any): Model output;
        
        Returns:
            Dict[str, Any]: Expected keys:
                "label" (Optional[Tuple[str, float]]): Label with highest score,
                    if score higher or equal to threshold, else - None.
        """
        labels = super().execute(input_data)["labels"]
        sorted_labels = sorted(labels.items(), key=(lambda a: a[1]), reverse=True)
        return {
            "label": sorted_labels[0] if sorted_labels else None
        }