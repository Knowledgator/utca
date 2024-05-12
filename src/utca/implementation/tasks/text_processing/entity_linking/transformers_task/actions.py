from typing import (
    Any, Dict, List, Optional, Tuple, Union, cast
)

import torch
from transformers import ( # type: ignore
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
)

from utca.core.executable_level_1.actions import (
    Action
)

class EntityLinkingPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Prepare prompts for model

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "texts" (List[str]): Texts to process;

    Returns:
        Dict[str, Any]: Expected keys:
            "texts" (Any): Prompts;
    """
    prompt: str = "Classifity the following text:\n {}\nLabel:"

    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "texts" (List[str]): Texts to process;

        Returns:
            Dict[str, Any]: Expected keys:
                "texts" (Any): Prompts;
        """
        return {
            "texts": [
                self.prompt.format(text)
                for text in input_data["texts"]
            ]
        }    


class EntityLinkingPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Process model output

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "sequences" (Any): Model output;

            "sequences_scores" (Optional[Any], optional): Used if num_beams > 1. Defaults to None;
            
            "num_beams" (int);
            
            "texts" (List[str]): Processed prompts;
    Returns:
        Dict[str, Any]: Expected keys:
            "classification_output" (Any): Formatted output;
    """
    def __init__(
        self, 
        tokenizer: Union[PreTrainedTokenizer, PreTrainedTokenizerFast],
        encoder_decoder: bool,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            tokenizer (Union[PreTrainedTokenizer, PreTrainedTokenizerFast])

            encoder_decoder (bool): Model configuration parameter.
            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.tokenizer = tokenizer
        self.encoder_decoder = encoder_decoder


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        decodes = self.tokenizer.batch_decode( # type: ignore
            input_data["sequences"], # type: ignore
            skip_special_tokens=True
        )

        num_beams = input_data["num_beams"]
        if num_beams > 1:
            scores = input_data["sequences_scores"] # type: ignore
        else:
            scores = torch.ones(len(decodes))
        
        outputs2scores: List[List[Tuple[str, float]]] = []
        for text_id in range(len(input_data["texts"])):
            input_ = input_data["texts"][text_id]
            input_len = len(input_)
            batch: List[Tuple[str, float]] = []
            for beam_id in range(num_beams):
                score = scores[text_id*num_beams+beam_id]
                p = torch.exp(score).item() # type: ignore
                label = cast(str, decodes[text_id*num_beams+beam_id])
                if not self.encoder_decoder:
                    label = label[input_len:].strip()
                batch.append((label, p))
            outputs2scores.append(batch)
        return {"classification_output": outputs2scores}