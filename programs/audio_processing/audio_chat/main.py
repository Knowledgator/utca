import pathlib
PATH = pathlib.Path(__file__).parent.resolve()

from utca.core import RenameAttribute, SetValue, ExecuteFunction
from utca.implementation.predictors import (
    OpenAIWhisperPredictor,
    WhisperModelConfig,
    OpenAIChatGPTPredictor,
    ChatGPTConfig,
)
from utca.implementation.tasks import (
    TransformersTextToSpeech, OpenAIChat
)
from utca.implementation.datasources.audio import (
    AudioWrite, AudioRead
)

if __name__ == "__main__":
    pipeline = (
        AudioRead(dtype="float32")
        | OpenAIWhisperPredictor(
            model_cfg=WhisperModelConfig(name="base"),
        )
        | RenameAttribute("text", "prompt")
        | ExecuteFunction(lambda input_data: print(input_data)) # type: ignore
        | OpenAIChat(
            predictor=OpenAIChatGPTPredictor(
                chat_cfg=ChatGPTConfig(
                    model="table_extractor"
                )
            )
        )
        | RenameAttribute("message", "text_inputs")
        | SetValue("path_to_file", f"{PATH}/response.wav")
        | TransformersTextToSpeech()
        | AudioWrite()
    )

    pipeline.run({
        "path_to_file": f"{PATH}/request.wav"
    })
