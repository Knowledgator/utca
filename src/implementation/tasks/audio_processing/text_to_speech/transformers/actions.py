from typing import Any, Dict

from core.executable_level_1.actions import Action

class TextToSpeechPostprocess(Action[Dict[str, Any], Dict[str, Any]]):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "audio_data": input_data["outputs"]["audio"],
            "sampling_rate": input_data["outputs"]["sampling_rate"]
        }