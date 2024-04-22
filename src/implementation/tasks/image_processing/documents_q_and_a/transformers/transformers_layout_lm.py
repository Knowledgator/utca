from typing import Any, List, Type, Optional

from core.executable_level_1.schema import IOModel
from core.executable_level_1.actions import Action
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.task import Task
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig
)
from implementation.predictors.transformers.schema import (
    TransformersVisualQandAInput,
    TransformersBasicOutput
)
from implementation.tasks.image_processing.documents_q_and_a.transformers.actions import (
    DocumentQandAPostprocess
)


class DocumentQandAOutput(IOModel):
    answer: Optional[str]


class TransformersDocumentQandA(
    Task[
        TransformersVisualQandAInput, 
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
        input_class: Type[TransformersVisualQandAInput]=TransformersVisualQandAInput,
        output_class: Type[DocumentQandAOutput]=DocumentQandAOutput,
        name: Optional[str]=None,
    ) -> None:
        if not predictor:
            predictor = TransformersPipeline(
                TransformersPipelineConfig(
                    task="document-question-answering", 
                    model=self.default_model
                ),
                input_class=TransformersVisualQandAInput,
                output_class=TransformersBasicOutput
            )

        super().__init__(
            predictor=predictor,
            preprocess=preprocess or [],
            postprocess=postprocess or [DocumentQandAPostprocess()],
            input_class=input_class, 
            output_class=output_class,
            name=name,
        )
