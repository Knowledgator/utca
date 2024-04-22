from typing import Any, List, Callable, Optional

from pydantic import ConfigDict
from PIL import Image
import torch

from core.executable_level_1.schema import (
    Input, Output
)

class TransformersImageClassificationModelInput(Input):
    pixel_values: Any


class TransformersTextToSpeechInput(Input):
    text_inputs: str


class TransformersTextToSpeechOutput(Output):
    audio: Any
    sampling_rate: int


class TransformersChartsAndPlotsModelInput(Input):
    flattened_patches: Any
    attention_mask: Any


class TransformersVisualQandAInput(Input):
    model_config = ConfigDict(arbitrary_types_allowed=True)
        
    image: Image.Image
    question: str


class TransformersImageModelRawInput(Input):
    input_ids: Any
    token_type_ids: Any
    attention_mask: Any
    pixel_values: Any
    pixel_mask: Any


class TransformersEmbeddingInput(Input):
    encodings: Any


class TransformersEmbeddingOutput(Output):
    last_hidden_state: Any


class TransformersEntityLinkingInput(Input):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    encodings: Any
    num_beams: int
    num_return_sequences: int
    prefix_allowed_tokens_fn: Callable[
        [torch.Tensor, int], List[int]
    ]


class TransformersEntityLinkingOutput(Output):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sequences: Any
    sequences_scores: Optional[Any]=None


class TransformersTextualQandAInput(Input):
    question: str
    context: str


class TransformersTextualQandAOutput(Output):
    answer: Optional[str]=None
    score: float=0.


class TransformersBasicInput(Input):
    inputs: Any


class TransformersLogitsOutput(Output):
    logits: Any


class TransformersBasicOutput(Output):
    output: Any