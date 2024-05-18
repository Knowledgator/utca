from typing import Any, Dict, Mapping, Optional, Protocol, runtime_checkable

import torch
from transformers import DetrImageProcessor # type: ignore

from utca.core.executable_level_1.actions import Action
from utca.implementation.tasks.utils import ensure_attributes

@runtime_checkable
class Processor(Protocol):
    @classmethod
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        ...


class ObjectDetectionPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Prepare model input

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "image" (Image.Image): Image to analyze;

    Returns:
        Dict[str, Any]: Expected keys:
            "pixel_values" (Any);
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


class DETRPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Process model output

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "image" (Image.Image): Processed image;

            "logits" (Any): Model output;

            "pred_boxes" (Any);
    
    Returns:
        Dict[str, Any]: Expected keys:
            "scores" (List[float]): Probability scores.

            "labels" (List[str]): Classified labels.
            
            "boxes" (List[Tuple[float, float, float, float]]): Bounding boxes.
    """
    def __init__(
        self, 
        processor: DetrImageProcessor,
        labels: Mapping[Any, str],
        threshold: float = 0.5,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            processor (DetrImageProcessor): Feature extractor.
            
            threshold (float): Labels threshold score. Defaults to 0.5.
            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.processor = processor
        self.labels = labels
        self.threshold = threshold


    def execute(
        self, input_data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "image" (Image.Image): Processed image;

                "logits" (Any): Model output;

                "pred_boxes" (Any);
        
        Returns:
            Dict[str, Any]: Expected keys:
                "scores" (List[float]): Probability scores.
                "labels" (List[str]): Classified labels.
                "boxes" (List[Tuple[float, float, float, float]]): Bounding boxes.
        """
        target_sizes = torch.tensor([
            input_data["image"].size[::-1]
        ])
        results = self.processor.post_process_object_detection( # type: ignore
            ensure_attributes(input_data), 
            target_sizes=target_sizes, # type: ignore
            threshold=self.threshold,
        )[0]
        return {
            "scores": [score.item() for score in results["scores"]], # type: ignore
            "labels": [self.labels[label.item()] for label in results["labels"]], # type: ignore
            "boxes": [box.tolist() for box in results["boxes"]] # type: ignore
        }