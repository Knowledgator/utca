from typing import  Any, Dict, Optional, Type

import requests

from utca.core.executable_level_1.interpreter import Evaluator
from utca.core.executable_level_1.executable import Executable
from utca.core.executable_level_1.schema import (
    IOModel
)
from utca.implementation.schemas.web_scraping.web2meaning.schema import Web2MeaningParameters

class Web2MeaningInput(IOModel):
    url: str


class Web2MeaningOutput(IOModel):
    results: Dict[str, Any]


class Web2Meaning(
    Executable[
        Web2MeaningInput,
        Web2MeaningOutput
    ]
):
    """
    Web2Meaning API
    """
    
    def __init__(
        self, 
        rapid_api_key: str,
        cfg: Optional[Web2MeaningParameters]=None,
        input_class: Type[Web2MeaningInput]=Web2MeaningInput,
        output_class: Type[Web2MeaningOutput]=Web2MeaningOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            rapid_api_key (str): API access key.

            cfg (Optional[Web2MeaningParameters], optional): API parameters. 
            
            input_class (Type[Web2MeaningInput], optional): Class for input validation.
                Defaults to Web2MeaningInput.
            
            output_class (Type[Web2MeaningOutput], optional): Class for output validation.
                Defaults to Web2MeaningOutput.
           
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(
            input_class=input_class,
            output_class=output_class,
            name=name,
        )
        self.cfg = cfg or Web2MeaningParameters()
        self.api_endpoint = "https://web2meaning.p.rapidapi.com/parse/v2"
        self.headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": rapid_api_key,
            "X-RapidAPI-Host": "web2meaning.p.rapidapi.com"
        }


    def invoke(self, input_data: Web2MeaningInput, evaluator: Evaluator) -> Dict[str, Any]:
        return {
            "results": requests.post(
                self.api_endpoint, 
                json={"params": self.cfg.extract(), "url": input_data.url}, 
                headers=self.headers
            ).json()
        }