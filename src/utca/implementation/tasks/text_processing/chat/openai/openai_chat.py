from typing import Any, List, Generator, Type, Optional

from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam

from utca.core.executable_level_1.schema import IOModel, Input, Output
from utca.core.executable_level_1.executor import ActionType
from utca.core.task_level_3.task import Task
from utca.implementation.predictors.openai_chat_gpt.predictor import (
    OpenAIChatGPTPredictor
)
from utca.implementation.tasks.text_processing.chat.openai.actions import (
    ChatPreprocessor, ChatAddContext, ChatPostprocessor, ChatSaveContext
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
        messages: Optional[List[ChatCompletionMessageParam]]=None,
        preprocess: Optional[List[ActionType]]=None,
        postprocess: Optional[List[ActionType]]=None,
        input_class: Type[Input]=ChatInput,
        output_class: Type[Output]=ChatOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            predictor (Predictor[Any, Any]): Predictor that will be used in task. 
                If equals to None, default TokenSearcherPredictor will be used. 
                Defaults to None.

            preprocess (Optional[List[Action[Any, Any]]]): Chain of actions executed 
                before predictor. If equals to None, default chain will be used. 
                Defaults to None.

                Default chain:
                    [TokenSeatcherTextCleanerPreprocessor]
            
            postprocess (Optional[List[Action[Any, Any]]]): Chain of actions executed
                after predictor. If equals to None, default chain will be used.
                Defaults to None.

                Default chain:
                    [TokenSearcherTextCleanerPostprocessor]
            
            input_class (Type[Input]): Class for input validation. 
                Defaults to TokenSearcherTextCleanerInput.

            output_class (Type[NEROutputType]): Class for output validation. 
                Defaults to TokenSearcherTextCleanerOutput.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        if messages is None:
            messages = []
        super().__init__(
            predictor=predictor,
            preprocess=preprocess or [
                ChatPreprocessor(), 
                ChatAddContext(messages)
            ],
            postprocess=postprocess or [
                ChatPostprocessor().use(set_key="message"),
                ChatSaveContext(messages).use(get_key="message")
            ],
            input_class=input_class, 
            output_class=output_class,
            name=name,
        )