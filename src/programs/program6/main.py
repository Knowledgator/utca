from typing import List, Dict, Any

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
from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.schema import AddData, ExecuteFunction

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


def prepare_batch_image_classification_input(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    frames: List[Dict[str, Any]] = []
    ok, frame = state['video_data'].read()
    while ok:
        frames.append({'image': Image.fromarray(frame)}) # type: ignore
        ok, frame = state['video_data'].read()
    half = len(frames) // 2
    return [frames[0], frames[half//2], frames[half]]


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



pipeline = (
    Video().read()
    | ExecuteFunction(prepare_batch_image_classification_input)
    | model_stage
    | ExecuteFunction(interpret_results)
)

video_input = VideoReadInput(
    path_to_file='programs/program6/White Chicks - short.mp4'
)

print(Evaluator(pipeline).run_program(video_input))