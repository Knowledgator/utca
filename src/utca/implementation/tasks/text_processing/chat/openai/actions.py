from typing import Any, Dict, Generator

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

            "context" (Iterable[ChatCompletionMessageParam]): Context messages.

    Returns:
        Dict[str, Any]: Expected keys:
            "messages" (Iterable[ChatCompletionMessageParam]): Context messages
                and input messages.
    """
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "messages" (Iterable[ChatCompletionMessageParam]): Input messages.

                "context" (Iterable[ChatCompletionMessageParam]): Context messages.

        Returns:
            Dict[str, Any]: Expected keys:
                "messages" (Iterable[ChatCompletionMessageParam]): Context messages
                    and input messages.
        """
        return {
            "messages": [*input_data["context"], *input_data["messages"]],
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
    

class ChatUpdateContext(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Update chat context

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "message" (str): Response message.

            "context" (Iterable[ChatCompletionMessageParam]): Context.
    
    Returns: 
        Dict[str, Any]: Expected keys:
            "context" (Iterable[ChatCompletionMessageParam]): Updated context.
    """
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "message" (str): Response message.

                "context" (Iterable[ChatCompletionMessageParam]): Context.
        
        Returns: 
            Dict[str, Any]: Expected keys:
                "context" (Iterable[ChatCompletionMessageParam]): Updated context.
        """
        return {
            "context": [
                *input_data["context"], {"role": "assistant", "content": input_data["message"]}
            ]
        }