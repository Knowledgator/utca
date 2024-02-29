from typing import Dict, Any

from implementation.predictors.transformers.transformers_text_to_speech import (
    TransformersTextToSpeechConfig,
    TransformersTextToSpeechPipeline
)
from implementation.datasources.audio.actions import (
    AudioWrite
)
from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.actions import AddData, ExecuteFunction

def prepare_sample_data(state: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "audio_data": state["outputs"]["audio"],
        "sampling_rate": state["outputs"]["sampling_rate"]
    }

if __name__ == "__main__":
    # Define model stage
    model_stage = TransformersTextToSpeechPipeline( # type: ignore
        TransformersTextToSpeechConfig(
            model="suno/bark-small"
        )
    )

    pipeline = (
        model_stage
        | ExecuteFunction(prepare_sample_data)
        | AddData({"path_to_file": "programs/program5/test.wav"})
        | AudioWrite()
    )

    Evaluator(pipeline).run_program({
        "text": "Hello world!"
    })