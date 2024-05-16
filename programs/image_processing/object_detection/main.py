from typing import Any, Dict, Tuple
import pathlib
PATH = pathlib.Path(__file__).parent.resolve()
import random

from PIL import ImageDraw

from utca.core import ExecuteFunction, AddData
from utca.implementation.tasks import (
    TransformersObjectDetection
)
from utca.implementation.datasources.image import ImageRead, ImageWrite

def draw_bboxes_and_meta(input_data: Dict[str, Any]) -> None:
    draw = ImageDraw.Draw(input_data["image"]) # type: ignore
    labels_to_colors: Dict[str, Tuple[int, int, int]] = {}

    for bbox, label, score in zip(
        input_data["boxes"], input_data["labels"], input_data["scores"]
    ):
        if not label in labels_to_colors:
            labels_to_colors[label] = tuple(random.randint(0, 255) for _ in range(3)) # type: ignore
        draw.text( # type: ignore
            (bbox[0]+5, bbox[1]+5), 
            f"{label}: {score:.2}", 
            fill=labels_to_colors[label],
        )
        draw.rectangle( # type: ignore
            bbox, outline=labels_to_colors[label], width=3
        )

if __name__ == "__main__":
    pipeline = (
        ImageRead()
        | TransformersObjectDetection()
        | ExecuteFunction(draw_bboxes_and_meta)
        | AddData({"path_to_file": f"{PATH}/processed.jpg"})
        | ImageWrite()
    )

    pipeline.run({
        "path_to_file": f"{PATH}/test.jpg"
    }) # Result will be here: "{PATH}/processed.jpg"