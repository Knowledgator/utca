from typing import Any, Union, Dict, Optional, Type, Generic, TypeVar
from abc import ABC, abstractmethod
import string

from pydantic import BaseModel
from transformers import ( # type: ignore
    pipeline, AutoTokenizer, AutoModelForTokenClassification # type: ignore
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
    ) -> list[list[dict[str, Any]]]:
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


class Entity(BaseModel):
    start: int
    end: int
    span: str
    score: float


class BaseTokenSearcherConfig(TokenSearcherModelConfig):
    threshold: float=0.


class InputWithThreshold(Input):
    threshold: Optional[float]


InputWithThresholdType = TypeVar(
    'InputWithThresholdType', bound=InputWithThreshold
)


class BaseTokenSearcherOutput(Output):
    output: list[Entity]


BaseTokenSearcherOutputType = TypeVar(
    'BaseTokenSearcherOutputType', bound=BaseTokenSearcherOutput
)


class BaseTokenSearcher(
    TokenSearcherModel[
        BaseTokenSearcherConfig, 
        InputWithThresholdType, 
        BaseTokenSearcherOutputType
    ], 
    ABC
):
    input_data_type: Type[InputWithThresholdType]

    def __init__(self, cfg: BaseTokenSearcherConfig) -> None:
        super().__init__(cfg)


    def choose_threshold(self, input_data: InputWithThreshold):
        return (
            input_data.threshold 
            if not input_data.threshold is None 
            else self.cfg.threshold
        )
    

    @classmethod
    def clean_span(cls, prompt: str, start: int, end: int):
        junk = {*string.punctuation, *' \n\r\t'}
        while start != end - 1 and prompt[start] in junk:
            start += 1
        while end != start and prompt[end - 1] in string.punctuation:
            end -= 1
        return prompt[start:end], start, end


    def build_entity(
        self, text: str, raw_entity: Dict[str, Any], threshold: float 
    ) -> Union[Entity, None]:
        if raw_entity['score'] > threshold:
            span, start, end = self.clean_span(
                text, raw_entity['start'], raw_entity['end']
            )
            return Entity(
                start=start,
                end=end,
                span=span,
                score=raw_entity['score']
            )
        return None


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