from implementation.predictors.transformers.transformers_text_to_speech import (
    TransformersTextToSpeechConfig,
    TransformersTextToSpeechInput,
    TransformersTextToSpeechPipeline
)
from implementation.datasources.audio.audio import (
    Audio
)
from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.schema import AddData, ExecuteFunction

# Define model stage
model_stage = TransformersTextToSpeechPipeline( # type: ignore
    TransformersTextToSpeechConfig(
        model="suno/bark-small"
    )
)

pipeline = (
    model_stage
    | ExecuteFunction(lambda state: {
        'audio_data': state['outputs']['audio'],
        'sampling_rate': state['outputs']['sampling_rate']
    })
    | AddData({'path_to_file': 'programs/program5/test.wav'})
    | Audio().write()
)

text_to_speech_input = TransformersTextToSpeechInput(
    text='Hello world!'
)

Evaluator(pipeline).run_program(text_to_speech_input)