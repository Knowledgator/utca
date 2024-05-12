from typing import Any, Dict, Optional, Protocol, runtime_checkable

import torch
import numpy as np

from utca.core.executable_level_1.actions import Action

@runtime_checkable
class Tokenizer(Protocol):
    @classmethod
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        ...


class EmbeddingPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Prepare model input

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "texts" (List[str]): Texts to process;

    Returns:
        Dict[str, Any]: Expected keys:
            "encodings" (Any): Model inputs;
    """
    def __init__(
        self, tokenizer: Tokenizer, name: Optional[str]=None,
    ) -> None:
        """
        Args:
            tokenizer (Tokenizer): Tokenizer.

            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.tokenizer = tokenizer


    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "texts" (List[str]): Texts to process;

        Returns:
            Dict[str, Any]: Expected keys:
                "encodings" (Any): Model inputs;
        """
        return {
            "encodings": self.tokenizer(
                input_data["texts"], 
                padding=True, 
                truncation=True, 
                return_tensors="pt"
            )
        }

class EmbeddingPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Process model output

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "last_hidden_state" (Any): Model output;

    Returns:
        Dict[str, Any]: Expected keys:
            "embeddings" (Any);
    """
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "last_hidden_state" (Any): Model output;

        Returns:
            Dict[str, Any]: Expected keys:
                "embeddings" (Any);
        """
        texts_embeddings = input_data["last_hidden_state"][:, 0]
        # normalize embeddings
        texts_embeddings = torch.nn.functional.normalize(
            texts_embeddings, p=2, dim=1
        )
        return {"embeddings": texts_embeddings}


class ConvertEmbeddingsToNumpyArrays(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Convert embeddings to numpy arrays

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "embeddings" (Any);
    
    Returns:
        Dict[str, Any]: Expected keys:
            "embeddings" (Any);
    """
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "embeddings" (Any);
        
        Returns:
            Dict[str, Any]: Expected keys:
                "embeddings" (Any);
        """
        return {
            "embeddings": np.array([
                e.detach().numpy() for e in input_data["embeddings"]
            ])
        }
    