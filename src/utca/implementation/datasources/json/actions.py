from typing import Dict, Any
import json

from utca.core.executable_level_1.actions import Action

class JSONRead(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Read JSON
    """
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'path_to_file' (str): Path to JSON file;

        Returns:
            Dict[str, Any]: Expected keys:
                'json' (Any): JSON data;
        """
        with open(input_data["path_to_file"], "r") as f:
            return {
                "json": json.load(f)
            }


class JSONWrite(Action[Dict[str, Any], None]):
    """
    Write JSON
    """
    def execute(self, input_data: Dict[str, Any]) -> None:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'json' (Any): JSON data;

                'path_to_file' (str): Path to JSON file;
        """
        with open(input_data["path_to_file"], "w") as f:
            json.dump(input_data["json"], f)