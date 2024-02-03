from typing import Dict, Type, Any

from transformers import ( # type: ignore
    pipeline, AutoTokenizer, AutoModelForTokenClassification # type: ignore
)

from core.executable_level_1.schema import InputType, OutputType
from core.model_level_2.model import Model
from implementation.models.transformers_models.schema import (
    TransformersModelConfigType
)

class TransformersModel(
    Model[
        TransformersModelConfigType, 
        InputType, 
        OutputType
    ]
):
    input_data_type: Type[InputType]
    
    def __init__(self, cfg: TransformersModelConfigType) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(cfg.model) # type: ignore
        model = AutoModelForTokenClassification.from_pretrained(cfg.model) # type: ignore
        
        self.pipeline = pipeline(
            "ner", 
            model=model, # type: ignore
            tokenizer=self.tokenizer,
            aggregation_strategy='first', 
            batch_size=cfg.batch_size,
            device=cfg.device
        )
        super().__init__(cfg)


    def get_predictions(
        self, inputs: list[str]
    ) -> list[list[Dict[str, Any]]]:
        return self.pipeline(inputs) # type: ignore