from typing import  Any, Dict, List, Optional, Type

from requests_html import HTMLSession # type: ignore

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
        super().__init__(
            input_class=input_class,
            output_class=output_class,
            name=name,
        )
        self.session = HTMLSession()
        self.js_rendering = js_rendering


    def invoke(self, input_data: RequestsHTMLInput, evaluator: Evaluator) -> Dict[str, Any]:
        r = self.session.get(input_data.url)
        if self.js_rendering:
            r.html.render() # type: ignore
        return {
            "text": r.html.text, # type: ignore
            "links": r.html.links # type: ignore
        }