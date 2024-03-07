from typing import Type, Optional, Any, List, Union

from PIL import Image
from transformers import ( # type: ignore
    Pix2StructProcessor, Pix2StructForConditionalGeneration
)

from core.executable_level_1.schema import Config, Input, Output
from core.executable_level_1.actions import (
    OneToOne, OneToMany, ManyToOne, ManyToMany
)
from core.predictor_level_2.predictor import (
    Predictor, 
)
from core.predictor_level_2.schema import (
    PredictorConfig, PredictorInput, PredictorOutput
)
from core.task_level_3.task import Task
from implementation.predictors.transformers.transformers_model import (
    TransformersGenerativeModel, 
    TransformersModelConfig
)
from implementation.tasks.image_processing.charts_and_plots_analysis.transformers.actions import (
    ChartsAndPlotsAnalysisPreprocessor,
    ChartsAndPlotsAnalysisPreprocessorConfig,
    ChartsAndPlotsAnalysisPostprocessor,
    ChartsAndPlotsAnalysisPostprocessorConfig
)

class ChartsAndPlotsAnalysisInput(Input):
    class Config:
        arbitrary_types_allowed = True

    image: Image.Image
    text: str


class ChartsAndPlotsAnalysisOutput(Output):
    outputs: Any


class ModelInput(PredictorInput):
    flattened_patches: Any
    attention_mask: Any


class ChartsAndPlotsAnalysis(
    Task[
        Config,
        ChartsAndPlotsAnalysisInput, 
        ChartsAndPlotsAnalysisOutput
    ]
):
    default_model: str = "google/deplot"

    def __init__(
        self,
        *,
        cfg: Optional[Config]=None, 
        predictor: Optional[Predictor[
            PredictorConfig, 
            PredictorInput, 
            PredictorOutput
        ]]=None,
        preprocess: Optional[List[Union[OneToOne, OneToMany, ManyToOne, ManyToMany]]]=None,
        postprocess: Optional[List[Union[OneToOne, OneToMany, ManyToOne, ManyToMany]]]=None,
        input_class: Type[ChartsAndPlotsAnalysisInput]=ChartsAndPlotsAnalysisInput,
        output_class: Type[ChartsAndPlotsAnalysisOutput]=ChartsAndPlotsAnalysisOutput
    ) -> None:
        if not predictor:
            model = Pix2StructForConditionalGeneration.from_pretrained(self.default_model) # type: ignore
            predictor=TransformersGenerativeModel(
                TransformersModelConfig(
                    model=model, # type: ignore
                    kwargs={
                        "max_new_tokens": 512
                    }
                ),
                input_class=ModelInput
            )
        
        if not preprocess or not postprocess:
            processor = Pix2StructProcessor.from_pretrained(self.default_model) # type: ignore

            if not preprocess:
                preprocess=[
                    ChartsAndPlotsAnalysisPreprocessor(
                        ChartsAndPlotsAnalysisPreprocessorConfig(
                            processor=processor # type: ignore
                        )
                    )
                ]
            
            if not postprocess:
                postprocess=[
                    ChartsAndPlotsAnalysisPostprocessor(
                        ChartsAndPlotsAnalysisPostprocessorConfig(
                            processor=processor # type: ignore
                        )
                    )
                ]

        super().__init__(
            cfg=cfg,
            predictor=predictor, # type: ignore
            preprocess=preprocess,
            postprocess=postprocess,
            input_class=input_class, 
            output_class=output_class
        )