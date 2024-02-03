from typing import Dict, Any

from transformers import ( # type: ignore
    AutoTokenizer, AutoModelForTokenClassification # type: ignore
)

from core.executable_level_1.schema import Input, Output
from core.model_level_2.tranformers_schema import (
    TransformersPipelineConfig
)

class TokenSearcherModelConfig(TransformersPipelineConfig):
    name: str
    
    def __init__(self, name: str='knowledgator/UTC-DeBERTa-small', **kwargs: Dict[str, Any]):
        self.name = name
        super().__init__(
            task='ner', # type: ignore
            model=AutoModelForTokenClassification.from_pretrained(name), # type: ignore
            tokenizer=AutoTokenizer.from_pretrained(name), # type: ignore
            aggregation_strategy='first', # type: ignore
            batch_size=12, # type: ignore
            **kwargs
        )


class TokenSearcherModelInput(Input):
    inputs: list[str]


class TokenSearcherModelOutput(Output):
    inputs: list[str]
    outputs: list[list[Dict[str, Any]]]