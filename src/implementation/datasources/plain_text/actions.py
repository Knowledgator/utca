from typing import Dict, Any

from core.executable_level_1.actions import Action

class PlainTextRead(Action[Dict[str, Any], Dict[str, Any]]):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        with open(input_data["path_to_file"], "r") as f:
            return {
                "text": f.read()
            }


class PlainTextWrite(Action[Dict[str, Any], Dict[str, Any]]):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        with open(input_data["path_to_file"], "w") as f:
            f.write(input_data["text"])
        return input_data
    

class PlainTextAppend(Action[Dict[str, Any], Dict[str, Any]]):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        with open(input_data["path_to_file"], "a") as f:
            f.write(input_data["text"])
        return input_data