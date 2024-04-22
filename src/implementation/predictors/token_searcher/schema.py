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
    model: Optional[Union[
        str,
        PreTrainedModel,
        TFPreTrainedModel
    ]]="knowledgator/UTC-DeBERTa-small"
    tokenizer: Optional[Union[
        str,
        PreTrainedTokenizer
    ]]="knowledgator/UTC-DeBERTa-small"
    kwargs: Optional[Dict[str, Any]]={
        "aggregation_strategy": "first",
        "batch_size": 12
    }


class TokenSearcherPredictorInput(IOModel):
    inputs: List[str]


class TokenSearcherPredictorOutput(IOModel):
    output: List[List[Dict[str, Any]]]