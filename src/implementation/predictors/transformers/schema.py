from typing import Any, List, Callable, Optional

from pydantic import ConfigDict
from PIL import Image
import torch

from core.executable_level_1.schema import IOModel

class TransformersImageClassificationModelInput(IOModel):
    pixel_values: Any


class TransformersTextToSpeechInput(IOModel):
    text_inputs: str


class TransformersTextToSpeechOutput(IOModel):
    audio: Any
    sampling_rate: int


class TransformersChartsAndPlotsModelInput(IOModel):
    flattened_patches: Any
    attention_mask: Any


class TransformersVisualQandAInput(IOModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
        
    image: Image.Image
    question: str


class TransformersImageModelRawInput(IOModel):
    input_ids: Any
    token_type_ids: Any
    attention_mask: Any
    pixel_values: Any
    pixel_mask: Any


class TransformersEmbeddingInput(IOModel):
    encodings: Any


class TransformersEmbeddingOutput(IOModel):
    last_hidden_state: Any


class TransformersEntityLinkingInput(IOModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    encodings: Any
    num_beams: int
    num_return_sequences: int
    prefix_allowed_tokens_fn: Callable[
        [torch.Tensor, int], List[int]
    ]


class TransformersEntityLinkingOutput(IOModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sequences: Any
    sequences_scores: Optional[Any]=None


class TransformersTextualQandAInput(IOModel):
    question: str
    context: str


class TransformersTextualQandAOutput(IOModel):
    answer: Optional[str]=None
    score: float=0.


class TransformersBasicInput(IOModel):
    inputs: Any


class TransformersLogitsOutput(IOModel):
    logits: Any


class TransformersBasicOutput(IOModel):
    output: Any