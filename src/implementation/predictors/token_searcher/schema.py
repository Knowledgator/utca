from typing import Any, Dict, List, Union, Optional

from transformers import ( # type: ignore
    PreTrainedModel,
    TFPreTrainedModel,
    PreTrainedTokenizer,
)

from core.executable_level_1.schema import IOModel
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipelineConfig
)

class TokenSearcherPredictorConfig(TransformersPipelineConfig):
    task: Optional[str]="ner"
    """
    Transformers pipeline task
    """
    model: Optional[Union[
        str,
        PreTrainedModel,
        TFPreTrainedModel
    ]]="knowledgator/UTC-DeBERTa-small"
    """
    Model
    """
    tokenizer: Optional[Union[
        str,
        PreTrainedTokenizer
    ]]="knowledgator/UTC-DeBERTa-small"
    """
    Tokenizer
    """
    kwargs: Optional[Dict[str, Any]]={
        "aggregation_strategy": "first",
        "batch_size": 12
    }
    """
    Extra parameters
    """


class TokenSearcherPredictorInput(IOModel):
    inputs: List[str]
    """
    Text inputs
    """


class TokenSearcherPredictorOutput(IOModel):
    output: List[List[Dict[str, Any]]]
    """
    Entities of corresponding inputs
    """