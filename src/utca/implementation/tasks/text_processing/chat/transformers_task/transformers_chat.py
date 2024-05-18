from typing import Any, Type, Optional
import uuid

from utca.core.executable_level_1.actions import RenameAttribute
from utca.core.executable_level_1.component import Component
from utca.core.executable_level_1.memory import GetMemory, SetMemory
from utca.core.executable_level_1.schema import Input, Output
from utca.core.predictor_level_2.predictor import Predictor
from utca.core.task_level_3.task import Task
from utca.implementation.predictors.transformers_predictor.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig,
)
from utca.implementation.predictors.transformers_predictor.schema import (
    TransformersBasicInput, TransformersBasicOutput
)
from utca.implementation.tasks.text_processing.chat.schema import (
    ChatInput, ChatOutput
)
from utca.implementation.tasks.text_processing.chat.actions import (
    ChatAddContext, ChatUpdateContext
)
from utca.implementation.tasks.text_processing.chat.transformers_task.actions import (
    ChatPreprocessor, ChatPostprocessor
)

class TransformersChat(
    Task[Input, Output]
):
    default_model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Any, Any]]=None,
        messages: Optional[str]=None,
        preprocess: Optional[Component]=None,
        postprocess: Optional[Component]=None,
        input_class: Type[Input]=ChatInput,
        output_class: Type[Output]=ChatOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            predictor (Optional[Predictor[Any, Any]], optional): Predictor that will be used in task. 
                If equals to None, default predictor will be used. Defaults to None.

            messages (Optional[str], optional): Key to use to access memory for messages.
                If equals to None, a unique key will be generated. Defaults to None.

                ***Note***: This parameter will function correctly only 
                when using the default preprocessor and postprocessor.
            
            preprocess (Optional[Component]]): Component executed 
                before predictor. If equals to None, default component will be used. 
                Defaults to None.

                Default component:
                    ChatPreprocessor | GetMemory | ChatAddContext | SetMemory | RenameAttribute
            
            postprocess (Optional[Component]]): Component executed
                after predictor. If equals to None, default component will be used.
                Defaults to None.

                Default component:
                    ChatPostprocessor | GetMemory | ChatUpdateContext | SetMemory
            
            input_class (Type[Input]): Class for input validation. 
                Defaults to ChatInput.

            output_class (Type[NEROutputType]): Class for output validation. 
                Defaults to ChatOutput.
            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        if not predictor:
            predictor = TransformersPipeline(
                TransformersPipelineConfig(
                    task="text-generation", 
                    model=self.default_model,
                    kwargs={
                        "max_new_tokens": 256, 
                        "do_sample": True, 
                        "temperature": 0.3, 
                        "top_k": 50, 
                        "top_p": 0.95,
                    }
                ),
                input_class=TransformersBasicInput,
                output_class=TransformersBasicOutput
            )
        
        if messages is None:
            messages = uuid.uuid4().hex
        super().__init__(
            predictor=predictor,
            preprocess=preprocess or (
                ChatPreprocessor()
                | GetMemory([(messages, "context")], default={messages:[]})
                | ChatAddContext()
                | SetMemory(messages, "messages")
                | RenameAttribute("messages", "inputs")
            ),
            postprocess=postprocess or (
                ChatPostprocessor().use(set_key="message")
                | GetMemory([(messages, "context")])
                | ChatUpdateContext()
                | SetMemory(messages, "context")
            ),
            input_class=input_class,
            output_class=output_class,
            name=name,
        )