from typing import Any, Dict, List, Optional, Type

from transformers import AutoTokenizer, AutoModelForCausalLM # type: ignore

from utca.core.executable_level_1.component import Component
from utca.core.executable_level_1.schema import Input, Output, IOModel
from utca.core.predictor_level_2.predictor import Predictor
from utca.core.task_level_3.task import Task
from utca.implementation.predictors.transformers_predictor.transformers_model import (
    TransformersGenerativeModel,
    TransformersModelConfig
)
from utca.implementation.predictors.transformers_predictor.schema import (
    TransformersIdsInput,
    TransformersBasicOutput
)
from utca.implementation.tasks.text_processing.function_call.transformers_task.actions import (
    TransformersFunctionCallPreprocessor,
    TransformersFunctionCallPostprocessor
)

class TransformersFunctionCallInput(IOModel):
    text: str
    output_schema: Dict[str, Any]
    examples: Optional[List[Dict[str, Any]]] = None


class TransformersFunctionCall(
    Task[Input, Output]
):
    """
    Task for text classification
    """

    default_model: str = "numind/NuExtract-tiny"

    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[Component]=None,
        postprocess: Optional[Component]=None,
        input_class: Type[Input]=TransformersFunctionCallInput,
        output_class: Type[Output]=TransformersBasicOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            predictor (Optional[Predictor[Any, Any]]): Predictor that will be used in task. 
                If equals to None, default predictor will be used. Defaults to None.

            preprocess (Optional[Component]): Component executed
                before predictor. If equals to None, default component will be used. Defaults to None.

                Default component: 
                    EntityLinkingPreprocessor
            
            postprocess (Optional[Component]): Component executed
                after predictor. If equals to None, default component will be used. Defaults to None.

                Default component: 
                    EntityLinkingPostprocessor
            
            input_class (Type[Input]): Class for input validation. Defaults to ComprehendItPredictorInput.

            output_class (Type[Output]): Class for output validation. Defaults to ComprehendItPredictorOutput.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        if not predictor:
            predictor = TransformersGenerativeModel(
                TransformersModelConfig(
                    model=AutoModelForCausalLM.from_pretrained(self.default_model, trust_remote_code=True), # type: ignore
                ),
                input_class=TransformersIdsInput,
                output_class=TransformersBasicOutput
            )

        if not preprocess or not postprocess:
            tokenizer = AutoTokenizer.from_pretrained(self.default_model) # type: ignore
            if not preprocess:
                preprocess = TransformersFunctionCallPreprocessor(
                    tokenizer=tokenizer
                )
            if not postprocess:
                postprocess = TransformersFunctionCallPostprocessor(
                    tokenizer=tokenizer
                )

        super().__init__(
            predictor=predictor,
            preprocess=preprocess,
            postprocess=postprocess,
            input_class=input_class, 
            output_class=output_class,
            name=name,
        )