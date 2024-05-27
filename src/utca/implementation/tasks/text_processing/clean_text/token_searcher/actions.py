from typing import Any, Dict, Optional

from utca.core.executable_level_1.actions import Action
from utca.implementation.predictors.token_searcher.utils import (
    build_entity
)
from utca.core.task_level_3.objects.objects import (
    Entity
)

class TokenSearcherTextCleanerPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Create prompt with providied text

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "text" (str): Text to process;
    
    Returns:
        Dict[str, Any]: Expected keys:
            "inputs" (List[str]): Model inputs;
    """
    prompt: str = """
Clean the following text extracted from the web matching not relevant parts:

{text}
"""

    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "text" (str): Text to process;
        
        Returns:
            Dict[str, Any]: Expected keys:
                "inputs" (List[str]): Model inputs;
        """
        return {"inputs": [self.prompt.format(text=input_data["text"])]}


class TokenSearcherTextCleanerPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Format output and clean text if specified

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "output" (List[List[Dict[str, Any]]]): Model output;
            
            "inputs" (List[str]): Model inputs;
            
            "text" (str): Processed text;
        
    Returns:
        Dict[str, Any]: Expected keys:
            "text" (str): Processed text;

            "output" (List[Entity]): uninformative data;

            "cleaned_text" (Optional[str], optional): Cleaned text. Equals to None, 
                if clean was set to False.
    """
    def __init__(
        self, 
        clean: bool=False,
        threshold: float=0.,
        name: Optional[str]=None,
    ) -> None:
        """
        Arguments:
            clean (bool): Remove uninformative data from text. Defaults to False.
            
            threshold (float): Data threshold score. Defaults to 0.
            
            name (Optional[str], optional): Name for identification. If equals to None, 
                class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.clean = clean
        self.threshold = threshold


    @classmethod
    def clean_text(cls, text: str, junk: list[Entity]) -> str:
        clean = ""
        start = 0
        for ent in junk:
            clean += text[start:ent.start].strip() + " "
            start = ent.end
        clean += text[start:].strip()
        return clean


    def execute(
        self, input_data: Dict[str, Any], 
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "output" (List[List[Dict[str, Any]]]): Model output;
                
                "inputs" (List[str]): Model inputs;
                
                "text" (str): Processed text;
            
        Returns:
            Dict[str, Any]: Expected keys:
                "text" (str): Processed text;

                "output" (List[Entity]): uninformative data;

                "cleaned_text" (Optional[str], optional): Cleaned text. Equals to None, 
                    if clean was set to False.
        """
        junk = [
            entity
            for output in input_data["output"]
            for ent in output 
            if (entity := build_entity(
                input_data["inputs"][0],
                ent, 
                self.threshold
            ))
        ]
        return {
            "text": input_data["text"],
            "output": junk,
            "cleaned_text": (
                self.clean_text(input_data["text"], junk) 
                if self.clean else None
            )
        }