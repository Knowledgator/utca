from typing import Any, Dict, Optional, Protocol, runtime_checkable

from utca.core.executable_level_1.actions import Action

@runtime_checkable
class Processor(Protocol):
    @classmethod
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        ...


    def decode(self, *args: Any, **kwargs: Any) -> Any:
        ...


class ChartsAndPlotsAnalysisPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Prepare model input

    Arguments:
        input_data (Dict[str, Any]): Expected keys:
            "text" (str): Text prompt;

            "image" (Image.Image): Image to analyze;

    Returns:
        Dict[str, Any]: Expected keys:
            "flattened_patches" (Any);

            "attention_mask" (Any);

    """
    def __init__(
        self, 
        processor: Processor,
        name: Optional[str]=None
    ) -> None:
        """
        Arguments:
            processor (Processor): Feature extractor.

            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.processor = processor


    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self.processor(
            images=input_data["image"],
            text=input_data["text"],
            return_tensors="pt"
        ).data


class ChartsAndPlotsAnalysisPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Process model output

    Arguments:
        input_data (Dict[str, Any]): Expected keys:
            "output" (Any): Model output;
    Returns:
        Dict[str, Any]: Expected keys:
            "output" (str): Text representation of chart or plot;
    """
    def __init__(
        self, 
        processor: Processor,
        name: Optional[str]=None
    ) -> None:
        """
        Arguments:
            processor (Processor): Feature extractor.

            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.processor = processor


    def execute(
        self, input_data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        """
        Arguments:
            input_data (Dict[str, Any]): Expected keys:
                "output" (Any): Model output;
        Returns:
            Dict[str, Any]: Expected keys:
                "output" (str): Text representation of chart or plot;
        """
        return {
            "output": self.processor.decode(
                input_data["output"][0], 
                skip_special_tokens=True,
            ).replace("<0x0A>", "<br/>")
        }