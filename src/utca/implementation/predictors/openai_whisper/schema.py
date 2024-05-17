from typing import Any, Dict, Optional, Tuple, Union

import torch
from numpy.typing import NDArray
from pydantic import ConfigDict

from utca.core.executable_level_1.schema import IOModel, Config

class WhisperInput(IOModel):
    """
    Args:
        audio (NDArray[Any]): Audio waveform.

        initial_prompt (Optional[str], optional): Optional text to provide as a prompt 
            for the first window. This can be used to provide, or "prompt-engineer" 
            a context for transcription, e.g. custom vocabularies or proper nouns
            to make it more likely to predict those word correctly.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    audio: NDArray[Any]
    initial_prompt: Optional[str] = None


class WhisperOutput(IOModel):
    text: str


class WhisperModelConfig(Config):
    """
    Args:
        name (str, optional): One of the official model names listed by 
            whisper.available_models(), or path to a model checkpoint containing 
            the model dimensions and the model state_dict. Defaults to "base".
        
        device (Union[str, torch.device]): The PyTorch device to put the model into.
        
        download_root (Optional[str], optional): Path to download the model files; 
            by default, it uses "~/.cache/whisper".
        
        in_memory (bool, optional): Whether to preload the model weights into host memory.
            Defaults to False.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    name: str = "base"
    device: Optional[Union[str, torch.device]] = None
    download_root: Optional[str] = None
    in_memory: bool = False


class WhisperTranscriptionConfig(Config):
    """
    Args:
        verbose (Optional[bool]): Whether to display the text being decoded 
            to the console. If True, displays all the details, If False, 
            displays minimal details. If None, does not display anything.

        temperature (Union[float, Tuple[float, ...]]): Temperature for sampling. 
            It can be a tuple of temperatures, which will be successively used upon
            failures according to either compression_ratio_threshold or logprob_threshold.

        compression_ratio_threshold (float): If the gzip compression ratio is above this value,
            treat as failed.

        logprob_threshold (float): If the average log probability over sampled tokens is below 
            this value, treat as failed.

        no_speech_threshold (float): If the no_speech probability is higher than this value 
            AND the average log probability over sampled tokens is below logprob_threshold,
            consider the segment as silent.

        condition_on_previous_text (bool): If True, the previous output of the model is provided
            as a prompt for the next window; disabling may make the text inconsistent across 
            windows, but the model becomes less prone to getting stuck in a failure loop,
            such as repetition looping or timestamps going out of sync.

        word_timestamps (bool): Extract word-level timestamps using the cross-attention pattern
            and dynamic time warping, and include the timestamps for each word in each segment.

        prepend_punctuations (str): If word_timestamps is True, merge these punctuation symbols 
            with the next word.

        append_punctuations (str): If word_timestamps is True, merge these punctuation symbols 
            with the previous word.

        decode_options (Optional[Dict[str, Any]]): Keyword arguments to construct 
            DecodingOptions instances.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    verbose: Optional[bool] = None
    temperature: Union[float, Tuple[float, ...]] = (0, 0.2, 0.4, 0.6, 0.8, 1)
    compression_ratio_threshold: Optional[float] = 2.4
    logprob_threshold: Optional[float] = -1
    no_speech_threshold: Optional[float] = 0.6
    condition_on_previous_text: bool = True
    word_timestamps: bool = False
    prepend_punctuations: str = "\"'“¿([{-"
    append_punctuations: str = "\"'.。,，!！?？:：”)]}、"
    decode_options: Optional[Dict[str, Any]]=None

    @property
    def transcription_config(self) -> Dict[str, Any]:
        tmp = self.model_dump(exclude={"decode_options"})
        if self.decode_options:
            tmp.update(self.decode_options)
        return tmp