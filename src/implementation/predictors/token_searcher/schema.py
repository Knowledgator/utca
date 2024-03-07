from typing import Dict, Any, TypeVar

from transformers import ( # type: ignore
    AutoTokenizer, AutoModelForTokenClassification # type: ignore
)

from core.predictor_level_2.schema import (
    PredictorInput,
    PredictorOutput
)
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipelineConfig
)

class TokenSearcherPredictorConfig(TransformersPipelineConfig):
    task='ner'
    model='knowledgator/UTC-DeBERTa-small'
    tokenizer='knowledgator/UTC-DeBERTa-small'
    kwargs={
        "aggregation_strategy": "first",
        "batch_size": 12
    }


class TokenSearcherPredictorInput(PredictorInput):
    inputs: list[str]


class TokenSearcherPredictorOutput(PredictorOutput):
    inputs: list[str]
    outputs: list[list[Dict[str, Any]]]


TokenSearcherPredictorConfigType = TypeVar("TokenSearcherPredictorConfigType", bound=TokenSearcherPredictorConfig)
TokenSearcherPredictorInputType = TypeVar("TokenSearcherPredictorInputType", bound=TokenSearcherPredictorInput)
TokenSearcherPredictorOutputType = TypeVar("TokenSearcherPredictorOutputType", bound=TokenSearcherPredictorOutput)