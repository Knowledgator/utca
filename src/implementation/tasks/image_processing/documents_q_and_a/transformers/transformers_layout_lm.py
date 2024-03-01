from typing import Type, Optional, List

from PIL import Image

from core.executable_level_1.schema import (
    Config, Output
)
from core.executable_level_1.actions import (
    Action, InputState, OutputState
)
from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import (
    PredictorConfig,
    PredictorInput,
    PredictorOutput
)
from core.task_level_3.task import Task
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig
)
from implementation.tasks.image_processing.documents_q_and_a.transformers.actions import (
    DocumentQandAPostprocess
)

class DocumentQandAInput(PredictorInput):
    class Config:
        arbitrary_types_allowed = True

    image: Image.Image
    question: str


class DocumentQandAOutput(Output):
    answer: str


class DocumentQandATask(
    Task[
        Config,
        DocumentQandAInput, 
        DocumentQandAOutput,
    ]
):
    default_model = "impira/layoutlm-document-qa"

    def __init__(
        self,
        *,
        cfg: Optional[Config]=None, 
        predictor: Optional[Predictor[
            PredictorConfig, 
            PredictorInput, 
            PredictorOutput
        ]]=None,
        preprocess: Optional[List[Action[InputState, OutputState]]]=None,
        postprocess: Optional[List[Action[InputState, OutputState]]]=None,
        input_class: Type[DocumentQandAInput]=DocumentQandAInput,
        output_class: Type[DocumentQandAOutput]=DocumentQandAOutput
    ) -> None:
        if not predictor:
            predictor = TransformersPipeline(
                TransformersPipelineConfig(
                    task="document-question-answering", 
                    model=self.default_model
                ),
                input_class=DocumentQandAInput
            )

        super().__init__(
            cfg=cfg, 
            predictor=predictor,
            preprocess=preprocess or [],
            postprocess=postprocess or [DocumentQandAPostprocess()],
            input_class=input_class, 
            output_class=output_class,
        )
