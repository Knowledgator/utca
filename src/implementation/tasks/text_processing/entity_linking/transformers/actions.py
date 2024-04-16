from typing import (
    Any, Dict, List, Optional, Tuple, Union, cast
)

import torch
from transformers import ( # type: ignore
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
)

from core.executable_level_1.actions import (
    Action
)

class EntityLinkingPreprocessing(Action[Dict[str, Any], Dict[str, Any]]):
    prompt: str = "Classifity the following text:\n {}\nLabel:"

    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        input_data["texts"] = [
            self.prompt.format(text)
            for text in input_data["texts"]
        ]
        return input_data
    

class EntityLinkingPostprocess(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        tokenizer: Union[PreTrainedTokenizer, PreTrainedTokenizerFast],
        encoder_decoder: bool,
        name: Optional[str]=None,
    ) -> None:
        super().__init__(name)
        self.tokenizer = tokenizer
        self.encoder_decoder = encoder_decoder


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        decodes = self.tokenizer.batch_decode( # type: ignore
            input_data["sequences"], # type: ignore
            skip_special_tokens=True
        )

        num_beams = input_data["num_beams"]
        if num_beams <= 1:
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