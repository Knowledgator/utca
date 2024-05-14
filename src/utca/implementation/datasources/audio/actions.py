from typing import Dict, Any

import soundfile as sf # type: ignore
import numpy as np

from utca.core.executable_level_1.actions import Action

class AudioRead(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Read audio file

    Args:
        input_data (Dict[str, Any]): Data to process. Expected keys:
            'path_to_file' (str): Path to audio file;

    Returns:
        Dict[str, Any]: Audio data. Expected keys:
            'audio' (ndarray);
            
            'sampling_rate' (int);
    """
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Data to process. Expected keys:
                'path_to_file' (str): Path to audio file;

        Returns:
            Dict[str, Any]: Audio data. Expected keys:
                'audio' (ndarray);
                
                'sampling_rate' (int);
        """
        audio_data, samplerate = sf.read(input_data["path_to_file"]) # type: ignore 
        return {
            'audio': audio_data,
            'sampling_rate': samplerate
        }


class AudioWrite(Action[Dict[str, Any], None]):
    """
    Write audio data to file

    Args:
        input_data (Dict[str, Any]): Data to process. Expected keys:
            'path_to_file' (str): Path to audio file;

            'audio' (ndarray);
            
            'sampling_rate' (int);
    """
    def execute(self, input_data: Dict[str, Any]) -> None:
        """
        Args:
            input_data (Dict[str, Any]): Data to process. Expected keys:
                'path_to_file' (str): Path to audio file;

                'audio' (ndarray);
                
                'sampling_rate' (int);
        """
        sf.write( # type: ignore
            input_data["path_to_file"], 
            np.ravel(input_data["audio"]),
            input_data["sampling_rate"]
        )