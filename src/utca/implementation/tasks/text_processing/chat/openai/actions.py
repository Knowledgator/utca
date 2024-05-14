from typing import Any, Dict, List, Generator, Optional

from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam

from utca.core.executable_level_1.actions import Action


class ChatPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "prompt" (str): Input prompt

        Returns:
            Dict[str, Any]: Expected keys:
                "messages" (Iterable[ChatCompletionMessageParam]): Input messages.
        """
        return {
            "messages": [{
                "role": "user",
                "content": input_data["prompt"],
            }]
        }


class ChatAddContext(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Add context

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "messages" (Iterable[ChatCompletionMessageParam]): Input messages.

    Returns:
        Dict[str, Any]: Expected keys:
            "messages" (Iterable[ChatCompletionMessageParam]): Context messages
                and input messages.
    """
    def __init__(
        self, 
        messages: List[ChatCompletionMessageParam],
        name: Optional[str]=None
    ) -> None:
        super().__init__(name)
        self.messages = messages


    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "messages" (Iterable[ChatCompletionMessageParam]): Input messages.

        Returns:
            Dict[str, Any]: Expected keys:
                "messages" (Iterable[ChatCompletionMessageParam]): Context messages
                    and input messages.
        """
        self.messages.extend(input_data["messages"])
        return {
            "messages": self.messages
        }


class ChatPostprocessor(Action[Dict[str, Any], str]):
    """
    Process API output

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "choices" (List[Dict[str, Any]]): Expected keys:
                "message" (Dict[str, Any]): Expected keys:
                    "content" (str)

    Returns:
        str: Response message.
    """
    def execute(
        self, input_data: Dict[str, Any]
    ) -> str:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "choices" (List[Dict[str, Any]]): Expected keys:
                    "message" (Dict[str, Any]): Expected keys:
                        "content" (str)

        Returns:
            str: Response message.
        """
        return input_data["choices"][0]["message"]["content"] or ""
    

class ChatStreamPostprocessor(Action[Dict[str, Any], Generator[str, None, None]]):
    """
    Process API stream output

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "stream" (Iterable[Dict[str, Any]]): Expected keys:
                "choices" (List[Dict[str, Any]]): Expected keys:
                    "delta" (Dict[str, Any]): Expected keys:
                        "content" (str)

    Returns:
        Generator[str, None, None]: Response chunks.
    """
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Generator[str, None, None]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "stream" (Iterable[Dict[str, Any]]): Expected keys:
                    "choices" (List[Dict[str, Any]]): Expected keys:
                        "delta" (Dict[str, Any]): Expected keys:
                            "content" (str)

        Returns:
            Generator[str, None, None]: Response chunks.
        """
        return (
            chunk["choices"][0]["delta"]["content"] or "" 
            for chunk in input_data["stream"]
        )
    

class ChatSaveContext(Action[str, None]):
    """
    Save chat context
    
    Args:
        input_data (str): Response message.
    """
    def __init__(
        self, 
        messages: List[ChatCompletionMessageParam],
        name: Optional[str]=None
    ) -> None:
        super().__init__(name)
        self.messages = messages


    def execute(
        self, input_data: str
    ) -> None:
        """
        Args:
            input_data (str): Response message.
        """
        self.messages.append({"role": "assistant", "content": input_data})