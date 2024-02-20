from typing import Dict, Any, List

from PIL import Image
from transformers import ( # type: ignore
    AutoFeatureExtractor, 
    AutoModelForImageClassification,
    AutoConfig
)
import torch

from core.model_level_2.transformers_image_classification import (
    TransformersImageClassificationConfig,
    TransformersImageClassificationInput,
    TransformersImageClassification
)
from core.datasource_level_2.video import (
    Video,
    VideoReadInput
)
# from core.executable_level_1.interpreter import Evaluator
# from core.executable_level_1.schema import AddData, ExecuteFunction

model_name = "trpakov/vit-face-expression"

# Retrieve the id2label attribute from the configuration
labels = AutoConfig.from_pretrained( # type: ignore
    model_name
).id2label

# Define model stage
model_stage = TransformersImageClassification( # type: ignore
    TransformersImageClassificationConfig(
        model=AutoModelForImageClassification.from_pretrained(model_name), # type: ignore
        feature_extractor=AutoFeatureExtractor.from_pretrained(model_name) # type: ignore
    )
)

reader_output = Video().read().execute(
    VideoReadInput(path_to_file='programs/program6/White Chicks - short.mp4')
)


def prepare_batch_image_classification_input(state: Dict[str, Any]) -> Dict[str, Any]:
    frames: List[TransformersImageClassificationInput] = []
    ok, frame = reader_output.video_data.read()
    while ok:
        frames.append({'image': TransformersImageClassificationInput(
            Image.fromarray(frame) # type: ignore
        )})
        ok, frame = reader_output.video_data.read()
    return frames

outputs = model_stage.get_predictions(frames)

def interpret_results(model_ouput: Dict[str, Any]) -> Dict[str, Any]:
    probabilities = torch.nn.functional.softmax(
        model_ouput['outputs']['logits'], dim=-1
    )

    # Convert probabilities tensor to a Python list
    probabilities = probabilities.detach().numpy().tolist()[0]

    # Map class labels to their probabilities
    return {
        labels[i]: prob for i, prob in enumerate(probabilities)
    }



# pipeline = (
#     model_stage
#     | ExecuteFunction(lambda state: {
#         'audio_data': state['outputs']['audio'],
#         'sampling_rate': state['outputs']['sampling_rate']
#     })
#     | AddData({'path_to_file': 'programs/program5/test.wav'})
#     | Audio().write()
# )

# text_to_speech_input = TransformersTextToSpeechInput(
#     text='Hello world!'
# )

# Evaluator(pipeline).run_program(text_to_speech_input)