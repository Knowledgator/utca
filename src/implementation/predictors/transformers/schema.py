from typing import Any, Dict, List, Callable, Optional, TypeVar, Union

from pydantic import ConfigDict
from transformers import ( # type: ignore
    PreTrainedModel,
    TFPreTrainedModel,
    PretrainedConfig,
    PreTrainedTokenizer,
)
from transformers.image_processing_utils import ( # type: ignore
    BaseImageProcessor
)
from PIL import Image
import torch

from core.executable_level_1.schema import IOModel, Config

class TransformersModelConfig(Config):
    """
    Transformers model configuration
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: PreTrainedModel
    """
    Transformers model
    """
    kwargs: Optional[Dict[str, Any]]=None
    """
    Extra parameters
    """

    def get_kwargs(self) -> Dict[str, Any]:
        return self.kwargs or {}


class TransformersPipelineConfig(Config):
    """
    Transformers pipeline configuration
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True, 
        protected_namespaces=()
    )

    task: Optional[str]=None
    model: Optional[Union[
        str,
        PreTrainedModel,
        TFPreTrainedModel
    ]]=None
    config: Optional[Union[
        str,
        PretrainedConfig
    ]]=None
    tokenizer: Optional[Union[
        str,
        PreTrainedTokenizer
    ]]=None
    feature_extractor: Optional[Any]=None
    image_processor: Optional[Union[
        str, 
        BaseImageProcessor
    ]]=None
    framework: Optional[str]=None
    revision: Optional[str]=None
    use_fast: bool=True
    token: Optional[Union[str, bool]]=None
    device: Optional[Union[int, str, torch.device]]=None
    device_map: Optional[Union[
        str, 
        Dict[str, Union[int, str, torch.device]
    ]]]=None
    torch_dtype: Optional[Union[str, torch.dtype]]=None
    trust_remote_code: Optional[bool]=None
    model_kwargs: Optional[Dict[str, Any]]=None
    pipeline_class: Optional[Any]=None
    kwargs: Optional[Dict[str, Any]]=None


    @property
    def pipeline_config(self) -> Dict[str, Any]:
        tmp = self.model_dump(exclude={"kwargs"})
        if self.kwargs:
            tmp.update(self.kwargs)
        return tmp


class SummarizationInput(IOModel):
    inputs: List[str]
    """
    Text inputs
    """


SummarizationInputType = TypeVar(
    "SummarizationInputType",
    bound=SummarizationInput
)


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