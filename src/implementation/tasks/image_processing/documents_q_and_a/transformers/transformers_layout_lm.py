from typing import Any, List, Type, Optional

from PIL import Image

from core.executable_level_1.schema import (
    Input, Output
)
from core.executable_level_1.actions import Action
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.task import Task
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig
)
from implementation.tasks.image_processing.documents_q_and_a.transformers.actions import (
    DocumentQandAPostprocess
)

class DocumentQandAInput(Input):
    class Config:
        arbitrary_types_allowed = True

    image: Image.Image
    question: str


class DocumentQandAOutput(Output):
    answer: Optional[str]


class ModelOutput(Output):
    output: Any


class DocumentQandATask(
    Task[
        DocumentQandAInput, 
        DocumentQandAOutput,
    ]
):
    default_model = "impira/layoutlm-document-qa"

    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[List[Action[Any, Any]]]=None,
        postprocess: Optional[List[Action[Any, Any]]]=None,
        input_class: Type[DocumentQandAInput]=DocumentQandAInput,
        output_class: Type[DocumentQandAOutput]=DocumentQandAOutput
    ) -> None:
        if not predictor:
            predictor = TransformersPipeline(
                TransformersPipelineConfig(
                    task="document-question-answering", 
                    model=self.default_model
                ),
                input_class=DocumentQandAInput,
                output_class=ModelOutput
            )

        super().__init__(
            predictor=predictor,
            preprocess=preprocess or [],
            postprocess=postprocess or [DocumentQandAPostprocess()],
            input_class=input_class, 
            output_class=output_class,
        )
