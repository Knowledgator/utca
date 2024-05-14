from typing import Any, Dict, Optional, Type, cast

from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

from utca.core.executable_level_1.interpreter import Evaluator
from utca.core.executable_level_1.schema import Input, Output
from utca.core.predictor_level_2.predictor import Predictor
from utca.implementation.predictors.openai_chat_gpt.schema import (
    ChatGPTInput,
    ChatCompletionOutput,
    ChatGPTConfig,
)   
from utca.implementation.predictors.utils import ensure_dict

class OpenAIChatGPTPredictor(
    Predictor[Input, Output]
):
    """
    Basic ChatGPT predictor
    """
    def __init__(
        self,
        chat_cfg: ChatGPTConfig, 
        openai_client: Optional[OpenAI]=None,
        input_class: Type[Input]=ChatGPTInput,
        output_class: Type[Output]=ChatCompletionOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            chat_cfg (ChatGPTConfig): Chat configuration.

            openai_client (Optional[OpenAI], optional): OpenAI client that will be used.
                If equals to None, default OpenAI client will be used. Defaults to None.

            input_class (Type[Input], optional): Class for input validation.
                Defaults to ChatGPTInput.
            
            output_class (Type[Output], optional): Class for output validation.
                Defaults to ChatCompletionOutput.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(
            input_class=input_class,
            output_class=output_class,
            name=name,
        )
        self.client = openai_client or OpenAI()
        self.cfg = chat_cfg


    def invoke(self, input_data: Input, evaluator: Evaluator) -> Dict[str, Any]:
        res = self.client.chat.completions.create( # type: ignore
            **self.cfg.extract(),
            **input_data.extract(),
        )
        if self.cfg.stream == True:
            return ensure_dict(
                res,
                "stream"
            )
        return cast(ChatCompletion, res).model_dump()
    

    @property
    def config(self) -> ChatGPTConfig:
        """
        Chat configuration
        """
        return self.cfg
        