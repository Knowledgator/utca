from typing import List, Dict, Any

from PIL import Image, ImageDraw
from transformers import ( # type: ignore
    AutoImageProcessor, 
    AutoModelForImageClassification,
)
import numpy as np

from core import (
    ExecuteFunction
)
from implementation.predictors import (
    TransformersModel,
    TransformersModelConfig,
    TransformersImageClassificationModelInput,
    TransformersLogitsOutput
)
from implementation.tasks import (
    TransformersImageClassification,
    TransformersImageClassificationMultilabelOutput,
    ImageClassificationPreprocessor,
    ImageClassificationMultilabelPostprocessor,
)
from implementation.datasources.video import (
    VideoRead,
    VideoWrite
)

model_name = "trpakov/vit-face-expression"

model = AutoModelForImageClassification.from_pretrained(model_name) # type: ignore
processor = AutoImageProcessor.from_pretrained(model_name) # type: ignore
labels = model.config.id2label # type: ignore

# Define task stage
task = TransformersImageClassification(
    predictor=TransformersModel(
        TransformersModelConfig(
            model=model # type: ignore
        ),
        input_class=TransformersImageClassificationModelInput,
        output_class=TransformersLogitsOutput,
    ),
    preprocess=[
        ImageClassificationPreprocessor(
            processor=processor # type: ignore
        )
    ],
    postprocess=[
        ImageClassificationMultilabelPostprocessor(
            labels=labels # type: ignore
        )
    ],
    output_class=TransformersImageClassificationMultilabelOutput
)

def prepare_batch_image_classification_input(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    frames: List[Dict[str, Any]] = []
    ok, frame = state["video_data"].read()
    if not ok:
        raise ValueError("No video to read!")
    while ok:
        frames.append({"image": Image.fromarray(frame)}) # type: ignore
        ok, frame = state["video_data"].read()
    return [
        frames[i] for i in range(len(frames)//2, len(frames), 5)
    ]


def group_labels(state: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        output["labels"] for output in state
    ]


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
        "path_to_file": "programs/video_processing/frame_by_frame_emotion_detection/sample.avi",
        "frames": video_frames,
        "width": width,
        "height": height,
        "fourcc": "XVID", # https://fourcc.org/codecs.php
        "fps": 0.5
    }


if __name__ == "__main__":
    pipeline = (
        VideoRead()
        | ExecuteFunction(
            prepare_batch_image_classification_input
        ).use(set_key="frames")
        | task.use(get_key="frames", set_key="classifications")
        | ExecuteFunction(group_labels).use(
            get_key="classifications",
            set_key="labels"
        )
        | ExecuteFunction(prepare_sample)
        | VideoWrite()
    )

    pipeline.run({
        "path_to_file": "programs/video_processing/frame_by_frame_emotion_detection/White Chicks - short.mp4"
    })