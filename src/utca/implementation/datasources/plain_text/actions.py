from typing import Dict, Any

from utca.core.executable_level_1.actions import Action

class PlainTextRead(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Read plain text file
    """
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'path_to_file' (str): Path to plain text file;

        Returns:
            Dict[str, Any]: Expected keys:
                'text' (str): Text;
        """
        with open(input_data["path_to_file"], "r") as f:
            return {
                "text": f.read()
            }


class PlainTextWrite(Action[Dict[str, Any], None]):
    """
    Write plain text file
    """
    def execute(self, input_data: Dict[str, Any]) -> None:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'path_to_file' (str): Path to plain text file;

                'text' (str): Text to write;
        """
        with open(input_data["path_to_file"], "w") as f:
            f.write(input_data["text"])
    

class PlainTextAppend(Action[Dict[str, Any], None]):
    """
    Append to plain text file
    """
    def execute(self, input_data: Dict[str, Any]) -> None:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'path_to_file' (str): Path to plain text file;

                'text' (str): Text to append;
        """
        with open(input_data["path_to_file"], "a") as f:
            f.write(input_data["text"])