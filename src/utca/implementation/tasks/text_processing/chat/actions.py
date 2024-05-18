from typing import Any, Dict

from utca.core.executable_level_1.actions import Action


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
    

class ChatAddContext(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Add context to new messages

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