from typing import Any, Dict

from core.executable_level_1.actions import OneToOne

class TextToSpeechPostprocess(OneToOne):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "audio_data": input_data["outputs"]["audio"],
            "sampling_rate": input_data["outputs"]["sampling_rate"]
        }