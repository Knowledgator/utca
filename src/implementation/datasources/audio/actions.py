from typing import Dict, Any

import soundfile as sf # type: ignore
import numpy as np

from core.executable_level_1.actions import Action

class AudioRead(Action[Dict[str, Any], Dict[str, Any]]):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        audio_data, samplerate = sf.read(input_data["path_to_file"]) # type: ignore 
        return {
            'audio': audio_data,
            'sample_rate': samplerate
        }


class AudioWrite(Action[Dict[str, Any], Dict[str, Any]]):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        sf.write( # type: ignore
            input_data["path_to_file"], 
            np.ravel(input_data["audio"]),
            input_data["sampling_rate"]
        )
        return input_data