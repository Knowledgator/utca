import pathlib
PATH = pathlib.Path(__file__).parent.resolve()

from implementation.tasks.audio_processing.text_to_speech.transformers.transformers_text_to_speech import (
    TransformersTextToSpeech
)
from implementation.datasources.audio.actions import (
    AudioWrite
)
from core.executable_level_1.interpreter import Evaluator

if __name__ == "__main__":
    pipeline = (
        TransformersTextToSpeech()
        | AudioWrite()
    )

    Evaluator(pipeline).run_program({
        "text_inputs": "Hello world!",
        "path_to_file": f"{PATH}/test.wav"
    })