from typing import Any, Dict, Protocol, runtime_checkable

from core.executable_level_1.actions import Action
from core.executable_level_1.schema import Config

@runtime_checkable
class Processor(Protocol):
    @classmethod
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        ...


    def decode(self, *args: Any, **kwargs: Any) -> Any:
        ...


class ChartsAndPlotsAnalysisPreprocessorConfig(Config):
    class Config:
        arbitrary_types_allowed = True

    processor: Processor


class ChartsAndPlotsAnalysisPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        cfg: ChartsAndPlotsAnalysisPreprocessorConfig
    ) -> None:
        self.cfg = cfg


    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        res = self.cfg.processor(
            images=input_data["image"],
            text=input_data["text"],
            return_tensors="pt"
        )
        return res


class ChartsAndPlotsAnalysisPostprocessorConfig(Config):
    class Config:
        arbitrary_types_allowed = True

    processor: Processor


class ChartsAndPlotsAnalysisPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        cfg: ChartsAndPlotsAnalysisPostprocessorConfig
    ) -> None:
        self.cfg = cfg


    def execute(
        self, input_data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        return {
            "outputs": self.cfg.processor.decode(input_data["outputs"][0], skip_special_tokens=True).replace("<0x0A>", "<br/>")
        }