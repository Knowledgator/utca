from typing import Type, Optional, Any, List, Dict, Union

from PIL import Image

from core.executable_level_1.schema import Config, Input, Output
from core.executable_level_1.actions import (
    Action, InputState, OutputState
)
from core.task_level_3.task import Task
from implementation.predictors.transformers.transformers_model import (
    TransformersGenerativeModel
)
from implementation.tasks.charts_and_plots_analysis.actions import (
    ChartsAndPlotsAnalysisPreprocessor,
    ChartsAndPlotsAnalysisPostprocessor
)

class ChartsAndPlotsAnalysisInput(Input):
    def __init__(self, image: Image.Image, text: str, *_: Any, **__: Any):
        self.image: Image.Image = image
        self.text: str = text


    def __setattr__(self, name: str, value: Any) -> None: # disable pydantic
        self.__dict__[name] = value


    def model_dump(
        self, 
        *, 
        mode: str="python", 
        include: Optional[Union[
            set[int], set[str], dict[int, Any], dict[str, Any]
        ]]=None,
        exclude: Optional[Union[
            set[int], set[str], dict[int, Any], dict[str, Any]
        ]]=None,
        by_alias: bool=False, 
        exclude_unset: bool=False,
        exclude_defaults: bool=False,
        exclude_none: bool=False, 
        round_trip: bool=False,
        warnings: bool=True
    ) -> Dict[str, Any]:
        return {
            "image": self.image,
            "text": self.text
        }


class ChartsAndPlotsAnalysisOutput(Output):
    outputs: Any


class ChartsAndPlotsAnalysis(
    Task[
        Config,
        ChartsAndPlotsAnalysisInput, 
        ChartsAndPlotsAnalysisOutput
    ]
):
    input_class: Type[ChartsAndPlotsAnalysisInput] = ChartsAndPlotsAnalysisInput
    output_class: Type[ChartsAndPlotsAnalysisOutput] = ChartsAndPlotsAnalysisOutput
    
    def __init__(
        self,
        *,
        cfg: Optional[Config]=None, 
        predictor: TransformersGenerativeModel,
        preprocess: Optional[List[Action[InputState, OutputState]]]=None,
        postprocess: Optional[List[Action[InputState, OutputState]]]=None
    ) -> None:
        self.cfg = cfg
        self.predictor = predictor
        self._preprocess = preprocess or [ChartsAndPlotsAnalysisPreprocessor()]
        self._postprocess = postprocess or [ChartsAndPlotsAnalysisPostprocessor()]