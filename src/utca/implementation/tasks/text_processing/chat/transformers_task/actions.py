from typing import Any, Dict

from utca.core.executable_level_1.actions import Action

class ChatPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "prompt" (str): Input prompt;

        Returns:
            Dict[str, Any]: Expected keys:
                "messages" (Iterable[ChatCompletionMessageParam]): Input messages;
        """
        return {
            "messages": [{
                "role": "user",
                "content": input_data["prompt"],
            }]
        }


class ChatPostprocessor(Action[Dict[str, Any], str]):
    """
    Process API output

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "output" (List[Dict[str, Any]]): Expected keys:
                "generated_text" (str);

    Returns:
        str: Response message.
    """
    def execute(
        self, input_data: Dict[str, Any]
    ) -> str:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "output" (List[Dict[str, Any]]): Expected keys:
                    "generated_text" (str);

        Returns:
            str: Response message.
        """
        return input_data["output"][0]["generated_text"][-1]["content"]