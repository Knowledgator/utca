from typing import Dict, Any
import json

from core.executable_level_1.actions import OneToOne

class JSONRead(OneToOne):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        with open(input_data["path_to_file"], "r") as f:
            return {
                "json": json.load(f)
            }


class JSONWrite(OneToOne):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        with open(input_data["path_to_file"], "w") as f:
            json.dump(input_data["json"], f)
        return input_data