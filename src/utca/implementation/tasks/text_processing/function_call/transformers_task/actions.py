from typing import Any, Dict, List, Optional, Union
import json

import torch
from transformers import ( # type: ignore
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
)

from utca.core.executable_level_1.actions import Action

class TransformersFunctionCallPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Create prompt with provided text, schema, and examples 

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "text" (str): Text to process;

            "output_schema" (Dict[str, Any]): Output schema;

            "examples" (List[Dict[str, Any]]): Output examples;

    Returns:
        Dict[str, Any]: Expected keys:
            "input_ids" (torch.Tensor)

            "attention_mask" (torch.Tensor)
    """

    prompt = """<|input|>
### Template:
{schema}
{examples}
### Text:
{text}
<|output|>
"""

    def __init__(
        self, 
        tokenizer: Union[PreTrainedTokenizer, PreTrainedTokenizerFast],
        device: Union[str, torch.device] = "cpu",
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            tokenizer (Union[PreTrainedTokenizer, PreTrainedTokenizerFast]): Tokenizer to use.

            device (Union[str, torch.device]): Device to use. Defaults to "cpu".

            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.device = device
        self.tokenizer = tokenizer


    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "text" (str): Text to process;

                "output_schema" (Dict[str, Any]): Output schema;

                "examples" (List[Dict[str, Any]]): Output examples;

        Returns:
            Dict[str, Any]: Expected keys:
                "input_ids" (torch.Tensor)

                "attention_mask" (torch.Tensor)
        """
        schema = json.dumps(input_data["output_schema"], indent=4)
        examples: List[Dict[str, Any]] = input_data.get("examples") or []
        input_llm = self.prompt.format(
            schema=schema,
            examples="".join([
                f"### Example:\n{json.dumps(e, indent=4)}\n"
                for e in examples
            ]),
            text=input_data["text"]
        )
        encodings = self.tokenizer(
            input_llm, return_tensors="pt", truncation=True, max_length=4000
        ).to(self.device)
        return encodings.data # type: ignore


class TransformersFunctionCallPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Format output

    """

    def __init__(
        self, 
        tokenizer: Union[PreTrainedTokenizer, PreTrainedTokenizerFast],
        name: Optional[str]=None,
    ) -> None:
        """
        Arguments:
            threshold (float): Entities threshold score. Defaults to 0.
            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.      
        """
        super().__init__(name)
        self.tokenizer = tokenizer
    
    
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Arguments:
            input_data (Dict[str, Any]): Expected keys:
                "output" (torch.Tensor): Model output;

        Returns:
            Dict[str, Any]: Expected keys:
                "output" (Optional[Dict[str, Any]]): Deserialized output or None;
        """
        decoded = self.tokenizer.decode(input_data["output"][0], skip_special_tokens=True) # type: ignore
        
        if output_str := decoded.split("<|output|>", 1)[1].split("<|end-output|>", 1)[0]:
            return {
                "output": json.loads(output_str)
            }
        return {
            "output": None
        }