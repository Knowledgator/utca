from typing import  Any, Dict, List, Optional, Type
import logging

import requests
from pyquery import PyQuery as pq # type: ignore

from utca.core.executable_level_1.interpreter import Evaluator
from utca.core.executable_level_1.executable import Executable
from utca.core.executable_level_1.schema import (
    IOModel
)

class RequestsHTMLInput(IOModel):
    url: str


class RequestsHTMLOutput(IOModel):
    text: str
    links: List[str]


class RequestsHTML(Executable[RequestsHTMLInput, RequestsHTMLOutput]):
    """
    Basic requests-html scraper
    """
    def __init__(
        self,
        js_rendering: bool = False,
        input_class: Type[RequestsHTMLInput]=RequestsHTMLInput,
        output_class: Type[RequestsHTMLOutput]=RequestsHTMLOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            js_rendering (bool, optional): Specifies whether the page should be rendered.
                Defaults to False.

            input_class (Type[RequestsHTMLInput], optional): Class for input validation.
                Defaults to RequestsHTMLInput.
            
            output_class (Type[RequestsHTMLOutput], optional): Class for output validation.
                Defaults to RequestsHTMLOutput.
           
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        if js_rendering:
            logging.warning("The 'js_rendering' parameter is depricated and ignored.")
        super().__init__(
            input_class=input_class,
            output_class=output_class,
            name=name,
        )


    def invoke(self, input_data: RequestsHTMLInput, evaluator: Evaluator) -> Dict[str, Any]:
        d = pq(url=input_data.url, opener=lambda url, **_: requests.get(url).text) # type: ignore
        return {
            "text": d.text(), # type: ignore
            "links": list({a.attrib['href'] for a in d("a") if 'href' in a.attrib}) # type: ignore
        }