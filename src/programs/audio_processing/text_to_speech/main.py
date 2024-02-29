from implementation.tasks.audio_processing.text_to_speech.transformers.transformers_text_to_speech import (
    TransformersTextToSpeech
)
from implementation.datasources.audio.actions import (
    AudioWrite
)
from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.actions import AddData

if __name__ == "__main__":
    pipeline = (
        TransformersTextToSpeech()
        | AddData({"path_to_file": "programs/audio_processing/text_to_speech/test.wav"})
        | AudioWrite()
    )

    Evaluator(pipeline).run_program({
        "text_inputs": "Hello world!"
    })