from typing import Any, Dict, Protocol, runtime_checkable

import torch
import numpy as np

from core.executable_level_1.actions import Action
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


class EmbeddingPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(self, cfg: EmbeddingPreprocessorConfig) -> None:
        self.cfg = cfg


    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        input_data["encodings"] = self.cfg.tokenizer(
            input_data["texts"], 
            padding=True, 
            truncation=True, 
            return_tensors='pt'
        )
        return input_data
    

class EmbeddingPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        texts_embeddings = input_data["last_hidden_state"][:, 0]
        # normalize embeddings
        texts_embeddings = torch.nn.functional.normalize(
            texts_embeddings, p=2, dim=1
        )
        input_data["embeddings"] = texts_embeddings
        return input_data


class ConvertEmbeddingsToNumpyArrays(Action[Dict[str, Any], Dict[str, Any]]):
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        input_data["embeddings"] = np.array([
            e.detach().numpy() for e in input_data["embeddings"]
        ])
        return input_data
    