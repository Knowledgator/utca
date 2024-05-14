from typing import Any, Dict, Mapping, Optional, Protocol, runtime_checkable

import torch

from utca.core.executable_level_1.actions import Action

@runtime_checkable
class Processor(Protocol):
    @classmethod
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        ...


class VisualQandAPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Prepare model input

    Arguments:
        input_data (Dict[str, Any]): Expected keys:
            "image" (Image.Image): Image to analyze;

            "question" (str): Question to answer;
    
    Returns:
        Dict[str, Any]: Expected keys:
            "input_ids" (Any);

            "token_type_ids" (Any);
            
            "attention_mask" (Any);
            
            "pixel_values" (Any);
            
            "pixel_mask" (Any);
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
        Arguments:
            input_data (Dict[str, Any]): Expected keys:
                "image" (Image.Image): Image to analyze;

                "question" (str): Question to answer;
        
        Returns:
            Dict[str, Any]: Expected keys:
                "input_ids" (Any);

                "token_type_ids" (Any);
                
                "attention_mask" (Any);
                
                "pixel_values" (Any);
                
                "pixel_mask" (Any);
        """
        return self.processor(
            images=input_data["image"],
            text=input_data["question"],
            return_tensors="pt"
        ).data


class VisualQandAMultianswerPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Process model output

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "logits" (Any): Model output;
        
    Returns:
        Dict[str, Any]: Expected keys:
            "answers" (Dict[str, float]): Classified labels and scores.
    """
    def __init__(
        self, 
        labels: Mapping[Any, str],
        threshold: float = 0.,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            labels (List[str]): Labels for classification.

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
        Process model output

        Args:
            input_data (Dict[str, Any]): Expected keys:
                "logits" (Any): Model output;
            
        Returns:
            Dict[str, Any]: Expected keys:
                "answers" (Dict[str, float]): Classified labels and scores.
        """
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
    """
    Process model output

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "logits" (Any): Model output;
        
    Returns:
        Dict[str, Any]: Expected keys:
            "answer" (Optional[Tuple[str, float]]): Answer with highest score, 
                if score higher or equal to threshold, else - None.
    """
    def execute(
        self, input_data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "logits" (Any): Model output;
            
        Returns:
            Dict[str, Any]: Expected keys:
                "answer" (Optional[Tuple[str, float]]): Answer with highest score, 
                    if score higher or equal to threshold, else - None.
        """
        answers = super().execute(input_data)["answers"]
        sorted_answers = sorted(answers.items(), key=(lambda a: a[1]), reverse=True)
        return {
            "answer": sorted_answers[0] if sorted_answers else None
        }