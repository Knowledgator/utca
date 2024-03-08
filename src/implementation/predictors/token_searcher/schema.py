from typing import Any, Dict, List, TypeVar, Union, Optional

from transformers import ( # type: ignore
    PreTrainedModel,
    TFPreTrainedModel,
    PreTrainedTokenizer,
)
from core.predictor_level_2.schema import (
    PredictorInput,
    PredictorOutput
)
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


class TokenSearcherPredictorInput(PredictorInput):
    inputs: List[str]


class TokenSearcherPredictorOutput(PredictorOutput):
    inputs: List[str]
    outputs: List[List[Dict[str, Any]]]


TokenSearcherPredictorConfigType = TypeVar("TokenSearcherPredictorConfigType", bound=TokenSearcherPredictorConfig)
TokenSearcherPredictorInputType = TypeVar("TokenSearcherPredictorInputType", bound=TokenSearcherPredictorInput)
TokenSearcherPredictorOutputType = TypeVar("TokenSearcherPredictorOutputType", bound=TokenSearcherPredictorOutput)