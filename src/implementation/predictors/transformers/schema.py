from typing import Any

from core.executable_level_1.schema import (
    Input, Output
)

class TransformersImageClassificationModelInput(Input):
    pixel_values: Any


class TransformersImageClassificationModelOutput(Output):
    logits: Any