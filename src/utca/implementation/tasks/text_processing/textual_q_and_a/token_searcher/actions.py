from typing import Any, Dict, Optional

from utca.core.executable_level_1.actions import Action
from utca.implementation.predictors.token_searcher.utils import (
    build_entity
)

class TokenSearcherQandAPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Create prompt

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "text" (str): Text to process;

            "question" (str): Question to answer.
    Returns:
        Dict[str, Any]: Expected keys:
            "inputs" (List[str]): Model inputs;
    """
    prompt: str = """{question}
Text:
{text}"""
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "text" (str): Text to process;
                
                "question" (str): Question to answer.
        Returns:
            Dict[str, Any]: Expected keys:
                "inputs" (List[str]): Model inputs;
        """
        return {
            "inputs": [
                self.prompt.format(
                    question=input_data["question"],
                    text=input_data["text"],
                ) 
            ]
        }
    

class TokenSearcherQandAPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Format output

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "output" (List[List[Dict[str, Any]]]): Model output;

            "inputs" (List[str]): Model inputs;

            "text" (str): Processed text;

            "question" (str): Answered question.

    Returns:
        Dict[str, Any]: Expected keys:
            "text" (str): Processed text;

            "question" (str): Answered question.
            
            "output" (List[Entity]): Answers;
    """
    def __init__(
        self, 
        threshold: float = 0.,
        name: Optional[str]=None,
    ) -> None:
        """               
        Arguments:
            threshold (float): Answers threshold score. Defaults to 0.

            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.threshold = threshold
    
    
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            'text': input_data["text"],
            'question': input_data["question"],
            'output': [
                entity
                for output in input_data["output"]
                for ent in output 
                if (entity := build_entity(
                    input_data["inputs"][0],
                    ent,
                    self.threshold
                ))
            ]
        }