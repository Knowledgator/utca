from typing import Dict, Any

from transformers import ( # type: ignore
    AutoTokenizer, AutoModelForTokenClassification # type: ignore
)

from core.executable_level_1.schema import Input, Output
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


class TokenSearcherPredictorInput(Input):
    inputs: list[str]


class TokenSearcherPredictorOutput(Output):
    inputs: list[str]
    outputs: list[list[Dict[str, Any]]]