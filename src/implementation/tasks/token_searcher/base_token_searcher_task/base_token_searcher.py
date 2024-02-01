from typing import Any, Union, Dict, Optional, Type, Generic, TypeVar, Sequence
from abc import ABC, abstractmethod

from pydantic import BaseModel
from transformers import ( # type: ignore
    pipeline, AutoTokenizer, AutoModelForTokenClassification # type: ignore
)

from implementation.tasks.token_searcher.base_token_searcher_task.objects import (
    Entity, ClassifiedEntity
)

class Input(BaseModel, ABC):
    pass

class Output(BaseModel, ABC):
    pass

class Config(BaseModel, ABC):
    pass

InputType = TypeVar('InputType', bound=Input)
OutputType = TypeVar('OutputType', bound=Output, covariant=True)
ConfigType = TypeVar('ConfigType', bound=Config, contravariant=True)

class TokenSearcherModelConfig(Config):
    model_name: str
    sents_batch: int=10
    batch_size: int=12
    device: str='cpu'

TokenSearcherModelConfigType = TypeVar(
    'TokenSearcherModelConfigType', bound=TokenSearcherModelConfig, contravariant=True)


class Model(Generic[ConfigType, InputType, OutputType], ABC):
    input_data_type: Type[InputType]

    def __init__(self, cfg: ConfigType):
        self.cfg = cfg


class TokenSearcherModel(Model[TokenSearcherModelConfigType, InputType, OutputType]):
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
        input_data = (
            input_data
            if isinstance(input_data, type(InputType)) 
            else self.input_data_type.parse_obj(input_data)
        )
        return input_data


class BaseTokenSearcherConfig(TokenSearcherModelConfig):
    threshold: float=0.


BaseTokenSearcherConfigType = TypeVar(
    'BaseTokenSearcherConfigType', bound=BaseTokenSearcherConfig
)



class InputWithThreshold(Input):
    threshold: Optional[float]


InputWithThresholdType = TypeVar(
    'InputWithThresholdType', bound=InputWithThreshold
)

EntityType = TypeVar('EntityType', bound=Entity)

class BaseTokenSearcherOutput(Generic[EntityType], Output):
    output: Sequence[EntityType]


BaseTokenSearcherOutputType = TypeVar(
    'BaseTokenSearcherOutputType', 
    bound=Union[
        BaseTokenSearcherOutput[Entity],
        BaseTokenSearcherOutput[ClassifiedEntity],
    ],
    covariant=True
)


class BaseTokenSearcher(
    TokenSearcherModel[
        BaseTokenSearcherConfigType, 
        InputWithThresholdType, 
        BaseTokenSearcherOutputType
    ], 
    ABC
):
    input_data_type: Type[InputWithThresholdType]

    def __init__(self, cfg: BaseTokenSearcherConfigType) -> None:
        super().__init__(cfg)


    def choose_threshold(self, input_data: InputWithThreshold):
        return (
            input_data.threshold 
            if not input_data.threshold is None 
            else self.cfg.threshold
        )
    

    def _preprocess(
        self, input_data: Union[InputWithThresholdType, Dict[str, Any]]
    ) -> InputWithThresholdType:
        input_data = super()._preprocess(input_data)
        input_data.threshold = self.choose_threshold(input_data)
        return input_data


    @abstractmethod
    def _process(
        self, input_data: InputWithThresholdType
    ) -> Any:
        pass


    @abstractmethod
    def _postprocess(
        self, 
        input_data: InputWithThresholdType, 
        predicts: Any
    ) -> BaseTokenSearcherOutputType:
        pass


    def execute(
        self, 
        input_data: Union[InputWithThresholdType, Dict[str, Any]]
    ) -> BaseTokenSearcherOutputType:
        input_data = self._preprocess(input_data)
        return self._postprocess(
            input_data,
            self._process(input_data)
        )