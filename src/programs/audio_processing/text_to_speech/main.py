import pathlib
PATH = pathlib.Path(__file__).parent.resolve()

from implementation.tasks import (
    TransformersTextToSpeech
)
from implementation.datasources.audio import (
    AudioWrite
)

pipeline = (
    TransformersTextToSpeech() | AudioWrite()
)

if __name__ == "__main__":
    pipeline.run({
        "text_inputs": "Hello world!",
        "path_to_file": f"{PATH}/test.wav"
    })