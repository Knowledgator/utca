from typing import Dict, Generic, Type, Any, Union
from abc import ABC, abstractmethod

from transformers import ( # type: ignore
    pipeline, AutoTokenizer, AutoModelForTokenClassification # type: ignore
)

from implementation.models.token_searcher.schema import (
    ConfigType, 
    InputType, 
    OutputType, 
    TokenSearcherModelConfigType,
    TokenSearcherModelConfig, 
    TokenSearcherModelInput, 
    TokenSearcherModelOutput
)

class Model(Generic[ConfigType, InputType, OutputType], ABC):
    input_data_type: Type[InputType]

    def __init__(self, cfg: ConfigType):
        self.cfg = cfg


    @abstractmethod
    def get_predictions(
        self, inputs: Any
    ) -> Any:
        ...


    @abstractmethod
    def _preprocess(
        self, input_data: Union[InputType, Dict[str, Any]]
    ) -> InputType:
        ...


    @abstractmethod
    def _process(
        self, input_data: InputType
    ) -> Any:
        ...


    @abstractmethod
    def _postprocess(
        self, 
        input_data: InputType, 
        predicts: Any
    ) -> OutputType:
        ...


    @abstractmethod
    def execute(
        self, 
        input_data: Union[InputType, Dict[str, Any]]
    ) -> OutputType:
        ...


class BaseTokenSearcherModel(
    Model[
        TokenSearcherModelConfigType, 
        InputType, 
        OutputType
    ]
):
    input_data_type: Type[InputType]
    
    def __init__(self, cfg: TokenSearcherModelConfigType) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(cfg.model_name) # type: ignore
        model = AutoModelForTokenClassification.from_pretrained(cfg.model_name) # type: ignore
        
        self.pipeline = pipeline(
            "ner", 
            model=model, # type: ignore
            tokenizer=self.tokenizer,
            aggregation_strategy='first', 
            batch_size=cfg.batch_size,
            device=cfg.device
        )
        super().__init__(cfg)


    def get_predictions(
        self, inputs: list[str]
    ) -> list[list[Dict[str, Any]]]:
        return self.pipeline(inputs) # type: ignore


    def _preprocess(
        self, input_data: Union[InputType, Dict[str, Any]]
    ) -> InputType:
        return (
            input_data
            if isinstance(input_data, type(InputType)) 
            else self.input_data_type.parse_obj(input_data)
        )


    @abstractmethod
    def _process(
        self, input_data: InputType
    ) -> list[list[Dict[str, Any]]]:
        ...


    @abstractmethod
    def _postprocess(
        self, 
        input_data: InputType, 
        predicts: Any
    ) -> OutputType:
        ...


    def execute(
        self, 
        input_data: Union[InputType, Dict[str, Any]]
    ) -> OutputType:
        input_data = self._preprocess(input_data)
        return self._postprocess(
            input_data,
            self._process(input_data)
        )
    

class TokenSearcherModel(
    BaseTokenSearcherModel[
        TokenSearcherModelConfig, 
        TokenSearcherModelInput, 
        TokenSearcherModelOutput
    ]
):
    input_data_type: Type[TokenSearcherModelInput] = TokenSearcherModelInput

    def _process(
        self, input_data: TokenSearcherModelInput
    ) -> list[list[Dict[str, Any]]]:
        return self.get_predictions(input_data.inputs)


    def _postprocess(
        self, 
        input_data: TokenSearcherModelInput, 
        predicts: Any
    ) -> TokenSearcherModelOutput:
        return TokenSearcherModelOutput(
            inputs=input_data.inputs,
            output=predicts
        )