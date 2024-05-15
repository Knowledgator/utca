from typing import Any, Type, Optional

from utca.core.executable_level_1.component import Component
from utca.core.executable_level_1.schema import IOModel, Input, Output
from utca.core.predictor_level_2.predictor import Predictor
from utca.core.task_level_3.task import Task
from utca.implementation.predictors.transformers_predictor.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig,
)
from utca.implementation.predictors.transformers_predictor.schema import (
    TransformersBasicOutput
)
from utca.implementation.tasks.text_processing.summarization.transformers_task.actions import (
    SummarizationPostprocess
)

class SummarizationInput(IOModel):
    inputs: str
    max_length: int = 200
    min_length: int = 100


class SummarizationOutput(IOModel):
    summary_text: str


class TransformersTextSummarization(
    Task[Input, Output]
):
    """
    Text summarization task
    """
    default_model = "facebook/bart-large-cnn"

    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[Component]=None,
        postprocess: Optional[Component]=None,
        input_class: Type[Input]=SummarizationInput,
        output_class: Type[Output]=SummarizationOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            predictor (Optional[Predictor[Any, Any]], optional): Predictor that will be used in task. 
                If equals to None, default predictor will be used. Defaults to None.
            
            preprocess (Optional[Component], optional): Component executed
                before predictor. Defaults to None.
            
            postprocess (Optional[Component], optional): Component executed
                after predictor. If equals to None, default component will be used. Defaults to None.

                Default component: 
                    SummarizationPostprocess
            
            input_class (Type[Input], optional): Class for input validation.
                Defaults to SummarizationInput.
            
            output_class (Type[Output], optional): Class for output validation.
                Defaults to SummarizationOutput.
            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        if not predictor:
            predictor = TransformersPipeline(
                TransformersPipelineConfig(
                    task="summarization", 
                    model=self.default_model,
                ),
                input_class=SummarizationInput,
                output_class=TransformersBasicOutput
            )

        super().__init__(
            predictor=predictor,
            preprocess=preprocess,
            postprocess=postprocess or SummarizationPostprocess(),
            input_class=input_class, 
            output_class=output_class,
            name=name,
        )