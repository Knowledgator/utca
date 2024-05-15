from typing import Any, Generator, Type, Optional

import uuid

from utca.core.executable_level_1.component import Component
from utca.core.executable_level_1.memory import GetMemory, SetMemory
from utca.core.executable_level_1.schema import IOModel, Input, Output
from utca.core.task_level_3.task import Task
from utca.implementation.predictors.openai_chat_gpt.predictor import (
    OpenAIChatGPTPredictor
)
from utca.implementation.tasks.text_processing.chat.openai.actions import (
    ChatPreprocessor, ChatAddContext, ChatPostprocessor, ChatUpdateContext
)

class ChatInput(IOModel):
    prompt: str


class ChatOutput(IOModel):
    message: str


class ChatStreamOutput(IOModel):
    stream: Generator[str, None, None]


class OpenAIChat(
    Task[Input, Output]
):
    def __init__(
        self,
        *,
        predictor: OpenAIChatGPTPredictor[Any, Any],
        messages: Optional[str]=None,
        preprocess: Optional[Component]=None,
        postprocess: Optional[Component]=None,
        input_class: Type[Input]=ChatInput,
        output_class: Type[Output]=ChatOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            predictor (Optional[Predictor[Any, Any]]): Predictor that will be used in task. 
                If equals to None, default TokenSearcherPredictor will be used. 
                Defaults to None.

            messages (Optional[str], optional): Key to use to access memory for messages.
                If equals to None, a unique key will be generated. Defaults to None.
                
            preprocess (Optional[Component]]): Component executed 
                before predictor. If equals to None, default component will be used. 
                Defaults to None.

                Default component:
                    ChatPreprocessor | GetMemory | ChatAddContext
            
            postprocess (Optional[Component]]): Component executed
                after predictor. If equals to None, default component will be used.
                Defaults to None.

                Default component:
                    ChatPostprocessor | GetMemory | ChatUpdateContext | SetMemory
            
            input_class (Type[Input]): Class for input validation. 
                Defaults to TokenSearcherTextCleanerInput.

            output_class (Type[NEROutputType]): Class for output validation. 
                Defaults to TokenSearcherTextCleanerOutput.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        if messages is None:
            messages = uuid.uuid4().hex
        super().__init__(
            predictor=predictor,
            preprocess=preprocess or (
                ChatPreprocessor()
                | GetMemory([(messages, "context")], default={messages:[]})
                | ChatAddContext()
                | SetMemory(messages, "messages")
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