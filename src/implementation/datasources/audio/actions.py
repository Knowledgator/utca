from typing import Dict, Any

import soundfile as sf # type: ignore
import numpy as np

from core.executable_level_1.actions import Action

class AudioRead(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Read audio file
    """
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Data to process. Expected keys:
                'path_to_file' (str): key with value of path to an audio file;

        Returns:
            Dict[str, Any]: Audio data. Dict with keys:
                'audio' (ndarray);
                
                'sample_rate' (int);
        """
        audio_data, samplerate = sf.read(input_data["path_to_file"]) # type: ignore 
        return {
            'audio': audio_data,
            'sample_rate': samplerate
        }


class AudioWrite(Action[Dict[str, Any], None]):
    """
    Write audio data to file
    """
    def execute(self, input_data: Dict[str, Any]) -> None:
        """
        Args:
            input_data (Dict[str, Any]): Data to process. Expected keys:
                'path_to_file' (str): key with value of path to an audio file;

                'audio' (ndarray);
                
                'sample_rate' (int);
        """
        sf.write( # type: ignore
            input_data["path_to_file"], 
            np.ravel(input_data["audio"]),
            input_data["sampling_rate"]
        )