from typing import List, Dict, Any

from PIL import Image, ImageDraw, ImageFont
from transformers import ( # type: ignore
    AutoFeatureExtractor, 
    AutoModelForImageClassification,
    AutoConfig
)
import torch
import cv2
import numpy as np

from core.model_level_2.transformers_image_classification import (
    TransformersImageClassificationConfig,
    TransformersImageClassification
)
from core.datasource_level_2.video import (
    Video,
    VideoReadInput
)
from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.schema import ExecuteFunction
from core.executable_level_1.memory import SetMemory, GetMemory

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
    VideoReadInput(path_to_file="programs/program6/White Chicks - short.mp4")
)


def prepare_batch_image_classification_input(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    frames: List[Dict[str, Any]] = []
    ok, frame = state["video_data"].read()
    while ok:
        frames.append({"image": Image.fromarray(frame)}) # type: ignore
        ok, frame = state["video_data"].read()
    return [
        frames[i] for i in range(len(frames)//2, len(frames), 5)
    ]


def interpret_results(state: List[Dict[str, Any]]) -> Dict[str, Any]:
    frames_labels: List[Dict[str, Any]] = []
    for s in state:
        probabilities = torch.nn.functional.softmax(
            s["outputs"]["logits"], dim=-1
        )

        # Convert probabilities tensor to a Python list
        probabilities = probabilities.detach().numpy().tolist()[0]

        # Map class labels to their probabilities
        frames_labels.append({
            labels[i]: prob for i, prob in enumerate(probabilities)
        })
    return {
        "labels": frames_labels
    }


def prepare_sample(state: Dict[str, Any]) -> Dict[str, Any]:
    # font = ImageFont.truetype("arial.ttf", 36)
    position = (20, 20)
    text_color = (255, 255, 255)

    video_frames = []
    for idx, frame in enumerate(state["frames"]):
        candidates = state["labels"][idx]
        highest = sorted(candidates.items(), key=(lambda a: a[1]), reverse=True)[0]
        draw = ImageDraw.Draw(frame["image"])
        draw.text(position, f"{highest[0]}: {highest[1]:.2}", fill=text_color) # font=font # type: ignore
        video_frames.append(np.array(frame["image"])) # type: ignore
    
    width, height = state["frames"][0]["image"].size
    return {
        "path_to_file": "programs/program6/sample.avi",
        "frames": video_frames,
        "width": width,
        "height": height,
        "fourcc": "XVID", # https://fourcc.org/codecs.php
        "fps": 0.5
    }


# # Save the modified image
# image.save("output_image.jpg")

# # Close the image file
# image.close()

pipeline = (
    Video().read()
    | ExecuteFunction(prepare_batch_image_classification_input)
    | SetMemory("frames")
    | model_stage
    | ExecuteFunction(interpret_results)
    | GetMemory(["frames"])
    | ExecuteFunction(prepare_sample)
    | Video().write()
)

video_input = VideoReadInput(
    path_to_file="programs/program6/White Chicks - short.mp4"
)

print(Evaluator(pipeline).run_program(video_input))