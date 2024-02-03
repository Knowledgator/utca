from typing import Dict, Any

from core.executable_level_1.schema import Input, Output
from implementation.models.transformers_models.schema import (
    TransformersModelConfig
)

class TokenSearcherModelConfig(TransformersModelConfig):
    ...


class TokenSearcherModelInput(Input):
    inputs: list[str]


class TokenSearcherModelOutput(Output):
    inputs: list[str]
    outputs: list[list[Dict[str, Any]]]