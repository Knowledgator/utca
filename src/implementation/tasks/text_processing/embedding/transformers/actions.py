from typing import Any, Dict, Protocol, runtime_checkable

import torch

from core.executable_level_1.actions import OneToOne
from core.executable_level_1.schema import Config

@runtime_checkable
class Tokenizer(Protocol):
    @classmethod
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        ...


class EmbeddingPreprocessorConfig(Config):
    class Config:
        arbitrary_types_allowed = True

    tokenizer: Tokenizer


class EmbeddingPreprocessor(OneToOne):
    def __init__(self, cfg: EmbeddingPreprocessorConfig) -> None:
        self.cfg = cfg


    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        input_data["encodings"] = self.cfg.tokenizer(
            input_data["sentences"], 
            padding=True, 
            truncation=True, 
            return_tensors='pt'
        )
        return input_data
    

class EmbeddingPostprocessor(OneToOne):
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        sentence_embeddings = input_data["outputs"]["last_hidden_state"][:, 0]
        # normalize embeddings
        sentence_embeddings = torch.nn.functional.normalize(
            sentence_embeddings, p=2, dim=1
        )
        return {
            "embeddings": sentence_embeddings
        }