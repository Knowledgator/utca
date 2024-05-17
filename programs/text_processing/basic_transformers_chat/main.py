from typing import Any, Dict

from utca.core import (
    Branch, 
    Evaluator, 
    ExecuteFunction, 
    Switch, 
    Transformable, 
    While, 
    BREAK,
)
from utca.implementation.tasks import TransformersChat

def get_input_from_user(_: Any) -> Dict[str, Any]:
    return {
        "prompt": input("User: ")
    }


def print_response(response: str) -> None:
    print("Chat:", response)


def quit_chat(input_data: Transformable, evaluator: Evaluator) -> bool:
    return input_data.get("prompt") == "\\q"


if __name__ == "__main__":
    pipeline = While(
        (
            ExecuteFunction(get_input_from_user)
            | Switch(
                Branch(
                    BREAK, condition=quit_chat, exit_branch=True
                ),
                Branch(
                    TransformersChat() 
                    | ExecuteFunction(print_response).use("message")
                )
            )
        )
    )

    pipeline.run()