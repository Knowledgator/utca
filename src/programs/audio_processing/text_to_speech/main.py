import pathlib
PATH = pathlib.Path(__file__).parent.resolve()

from implementation.tasks import (
    TransformersTextToSpeech
)
from implementation.datasources.audio import (
    AudioWrite
)

if __name__ == "__main__":
    pipeline = (
        TransformersTextToSpeech()
        | AudioWrite()
    )

    pipeline.run({
        "text_inputs": "Hello world!",
        "path_to_file": f"{PATH}/test.wav"
    })