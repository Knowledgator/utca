from typing import Any, Dict, Optional, Type

import whisper # type: ignore

from utca.core.executable_level_1.interpreter import Evaluator
from utca.core.executable_level_1.schema import Input, Output
from utca.core.predictor_level_2.predictor import Predictor
from utca.implementation.predictors.openai_whisper.schema import (
    WhisperTranscriptionConfig,
    WhisperModelConfig,
    WhisperInput,
    WhisperOutput,
)   

class OpenAIWhisperPredictor(
    Predictor[Input, Output]
):
    """
    Basic ChatGPT predictor
    """
    def __init__(
        self,
        *,
        model_cfg: WhisperModelConfig,
        transcription_cfg: Optional[WhisperTranscriptionConfig]=None,
        input_class: Type[Input]=WhisperInput,
        ouput_class: Type[Output]=WhisperOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            cfg (Union[
                OpenAIWhisperTranscriptionConfig,
                OpenAIWhisperTranslationConfig
            ]): Whisper configuration.

            input_class (Type[Input], optional): Class for input validation.
                Defaults to WhisperInput.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(
            input_class=input_class,
            output_class=ouput_class,
            name=name,
        )
        self.cfg = model_cfg
        self.model = whisper.load_model(**model_cfg.extract())
        self.transcription_cfg = transcription_cfg or WhisperTranscriptionConfig()


    def invoke(self, input_data: Input, evaluator: Evaluator) -> Dict[str, Any]:
        return self.model.transcribe( # type: ignore
            **self.transcription_cfg.transcription_config,
            **input_data.extract()
        )
    

    @property
    def config(self) -> WhisperModelConfig:
        """
        Whisper configuration
        """
        return self.cfg
        