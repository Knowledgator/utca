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
    name: str
    
    def __init__(
        self,
        *,
        name: str='knowledgator/UTC-DeBERTa-small', 
        **kwargs: Any
    ):
        self.name = name
        super().__init__(
            task='ner', # type: ignore
            model=AutoModelForTokenClassification.from_pretrained(name), # type: ignore
            tokenizer=AutoTokenizer.from_pretrained(name), # type: ignore
            aggregation_strategy='first', # type: ignore
            batch_size=12, # type: ignore
            **kwargs
        )


class TokenSearcherPredictorInput(PredictorInput):
    inputs: list[str]


class TokenSearcherPredictorOutput(PredictorOutput):
    inputs: list[str]
    outputs: list[list[Dict[str, Any]]]


TokenSearcherPredictorConfigType = TypeVar("TokenSearcherPredictorConfigType", bound=TokenSearcherPredictorConfig)
TokenSearcherPredictorInputType = TypeVar("TokenSearcherPredictorInputType", bound=TokenSearcherPredictorInput)
TokenSearcherPredictorOutputType = TypeVar("TokenSearcherPredictorOutputType", bound=TokenSearcherPredictorOutput)