from typing import Any, Type, Optional

from pydantic import ConfigDict
from PIL import Image
from transformers import ( # type: ignore
    Pix2StructProcessor, Pix2StructForConditionalGeneration
)

from utca.core.executable_level_1.component import Component
from utca.core.executable_level_1.schema import (
    IOModel, Input, Output
)
from utca.core.predictor_level_2.predictor import Predictor
from utca.core.task_level_3.task import Task
from utca.implementation.predictors.transformers_predictor.transformers_model import (
    TransformersGenerativeModel,
    TransformersModelConfig
)
from utca.implementation.predictors.transformers_predictor.schema import (
    TransformersChartsAndPlotsModelInput,
    TransformersBasicOutput
)
from utca.implementation.tasks.image_processing.charts_and_plots_analysis.transformers_task.actions import (
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
        preprocess: Optional[Component]=None,
        postprocess: Optional[Component]=None,
        input_class: Type[Input]=ChartsAndPlotsAnalysisInput,
        output_class: Type[Output]=TransformersBasicOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Arguments:
            predictor (Optional[Predictor[Any, Any]], optional): Predictor that will be used in task. If equals to None,
                default predictor will be used. Defaults to None.
            
            preprocess (Optional[Component], optional): Component executed before predictor.
                If equals to None, default component will be used. Defaults to None.

                Default component: 
                    ChartsAndPlotsAnalysisPreprocessor

                If default component is used, ChartsAndPlotsAnalysisPreprocessor will use Pix2StructProcessor from "google/deplot" model.
            
            postprocess (Optional[Component], optional): Component executed after predictor.
                If equals to None, default component will be used. Defaults to None.

                Default component: 
                    ChartsAndPlotsAnalysisPostprocessor

                If default component is used, ChartsAndPlotsAnalysisPostprocessor will use Pix2StructProcessor from "google/deplot" model.
            
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
            processor = Pix2StructProcessor.from_pretrained(predictor.config._name_or_path) # type: ignore

            if not preprocess:
                preprocess=ChartsAndPlotsAnalysisPreprocessor(
                    processor=processor # type: ignore
                )
            
            if not postprocess:
                postprocess=ChartsAndPlotsAnalysisPostprocessor(
                        processor=processor # type: ignore
                )

        super().__init__(
            predictor=predictor,
            preprocess=preprocess,
            postprocess=postprocess,
            input_class=input_class, 
            output_class=output_class,
            name=name,
        )