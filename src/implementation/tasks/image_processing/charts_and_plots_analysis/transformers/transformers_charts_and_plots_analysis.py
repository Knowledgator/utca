from typing import Any, List, Type, Optional

from pydantic import ConfigDict
from PIL import Image
from transformers import ( # type: ignore
    Pix2StructProcessor, Pix2StructForConditionalGeneration
)

from core.executable_level_1.schema import (
    IOModel, Input, Output
)
from core.executable_level_1.actions import Action
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.task import Task
from implementation.predictors.transformers.transformers_model import (
    TransformersGenerativeModel,
    TransformersModelConfig
)
from implementation.predictors.transformers.schema import (
    TransformersChartsAndPlotsModelInput,
    TransformersBasicOutput
)
from implementation.tasks.image_processing.charts_and_plots_analysis.transformers.actions import (
    ChartsAndPlotsAnalysisPreprocessor,
    ChartsAndPlotsAnalysisPostprocessor,
)

class ChartsAndPlotsAnalysisInput(IOModel):
    """
    Arguments:
        image (Image.Image): Image to analyze.

        text (str): Text prompt.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    image: Image.Image
    text: str


class TransformersChartsAndPlotsAnalysis(
    Task[Input, Output]
):
    """
    Charts and plots analysis task
    """
    default_model: str = "google/deplot"

    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[List[Action[Any, Any]]]=None,
        postprocess: Optional[List[Action[Any, Any]]]=None,
        input_class: Type[Input]=ChartsAndPlotsAnalysisInput,
        output_class: Type[Output]=TransformersBasicOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Arguments:
            predictor (Predictor[Any, Any], optional): Predictor that will be used in task. If equals to None,
                default predictor will be used. Defaults to None.
            
            preprocess (Optional[List[Action[Any, Any]]], optional): Chain of actions executed before predictor.
                If equals to None, default chain will be used. Defaults to None.

                Default chain: 
                [ChartsAndPlotsAnalysisPreprocessor]

                If default chain is used, ChartsAndPlotsAnalysisPreprocessor will use Pix2StructProcessor from "google/deplot" model.
            
            postprocess (Optional[List[Action[Any, Any]]], optional): Chain of actions executed after predictor.
                If equals to None, default chain will be used. Defaults to None.

                Default chain: 
                [ChartsAndPlotsAnalysisPostprocessor]

                If default chain is used, ChartsAndPlotsAnalysisPostprocessor will use Pix2StructProcessor from "google/deplot" model.
            
            input_class (Type[Input], optional): Class for input validation. Defaults to ChartsAndPlotsAnalysisInput.
            
            output_class (Type[Output], optional): Class for output validation. Defaults to TransformersBasicOutput.
            
            name (Optional[str], optional): Name for identification. If equals to None, class name will be used.
                Defaults to None.
        """
        if not predictor:
            model = Pix2StructForConditionalGeneration.from_pretrained(self.default_model) # type: ignore
            predictor=TransformersGenerativeModel(
                TransformersModelConfig(
                    model=model, # type: ignore
                    kwargs={
                        "max_new_tokens": 512
                    }
                ),
                input_class=TransformersChartsAndPlotsModelInput,
                output_class=TransformersBasicOutput
            )
        
        if not preprocess or not postprocess:
            processor = Pix2StructProcessor.from_pretrained(self.default_model) # type: ignore

            if not preprocess:
                preprocess=[
                    ChartsAndPlotsAnalysisPreprocessor(
                        processor=processor # type: ignore
                    )
                ]
            
            if not postprocess:
                postprocess=[
                    ChartsAndPlotsAnalysisPostprocessor(
                        processor=processor # type: ignore
                    )
                ]

        super().__init__(
            predictor=predictor,
            preprocess=preprocess,
            postprocess=postprocess,
            input_class=input_class, 
            output_class=output_class,
            name=name,
        )