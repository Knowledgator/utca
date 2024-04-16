from typing import Any, Dict, Optional, Protocol, runtime_checkable

from core.executable_level_1.actions import Action

@runtime_checkable
class Processor(Protocol):
    @classmethod
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        ...


    def decode(self, *args: Any, **kwargs: Any) -> Any:
        ...


class ChartsAndPlotsAnalysisPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        processor: Processor,
        name: Optional[str]=None
    ) -> None:
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
    def __init__(
        self, 
        processor: Processor,
        name: Optional[str]=None
    ) -> None:
        super().__init__(name)
        self.processor = processor


    def execute(
        self, input_data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        return self.processor.decode(input_data["output"][0], skip_special_tokens=True).replace("<0x0A>", "<br/>")