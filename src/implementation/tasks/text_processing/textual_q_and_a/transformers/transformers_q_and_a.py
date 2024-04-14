from typing import Any, List, Type, Optional

from core.executable_level_1.actions import Action
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.task import Task
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig
)
from predictors.transformers.schema import (
    TransformersTextualQandAInput,
    TransformersTextualQandAOutput
)
from implementation.tasks.text_processing.textual_q_and_a.transformers.actions import (
    QandAPostprocess
)

class TransformersTextualQandA(
    Task[
        TransformersTextualQandAInput, 
        TransformersTextualQandAOutput,
    ]
):
    default_model: str = "deepset/roberta-base-squad2"
    
    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[List[Action[Any, Any]]]=None,
        postprocess: Optional[List[Action[Any, Any]]]=None,
        input_class: Type[TransformersTextualQandAInput]=TransformersTextualQandAInput,
        output_class: Type[TransformersTextualQandAOutput]=TransformersTextualQandAOutput
    ) -> None:
        if not predictor:
            predictor = TransformersPipeline(
                TransformersPipelineConfig(
                    task="question-answering", 
                    model=self.default_model
                ),
                input_class=TransformersTextualQandAInput,
                output_class=TransformersTextualQandAOutput
            )

        super().__init__(
            predictor=predictor,
            preprocess=preprocess or [],
            postprocess=postprocess or [QandAPostprocess()],
            input_class=input_class, 
            output_class=output_class,
        )
