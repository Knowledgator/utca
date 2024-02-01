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

InputType = TypeVar('InputType', bound=Input)
OutputType = TypeVar('OutputType', bound=Output)


class TokenSearcherModelConfig(BaseModel):
    model_name: str
    sents_batch: int=10
    batch_size: int=12
    device: str='cpu'


class TokenSearcherModel(Generic[InputType, OutputType], ABC):
    input_data_type: Type[InputType]
    output_data_type: Type[OutputType]

    def __init__(self, cfg: TokenSearcherModelConfig) -> None:
        self.cfg = cfg

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


    def get_predictions(
        self, inputs: list[str]
    ) -> list[list[dict[str, Any]]]:
        return self.pipeline(inputs) # type: ignore



    def _preprocess(
        self, input_data: Union[InputType, Dict[str, Any]]
    ) -> InputType:
        input_data = (
            input_data
            if isinstance(input_data, self.input_data_type) 
            else self.input_data_type.parse_obj(input_data)
        )
        return input_data


class Entity(BaseModel):
    start: int
    end: int
    span: str
    score: float


class BaseTokenSearcherConfig(TokenSearcherModelConfig):
    model_name: str
    sents_batch: int=10
    batch_size: int=12
    device: str='cpu'
    threshold: float=0.


class InputWithThreshold(Input):
    threshold: Optional[float]


class BaseTokenSearcherOutput(Output):
    output: list[Entity]



class BaseTokenSearcher(
    TokenSearcherModel[InputWithThreshold, BaseTokenSearcherOutput],
):
    def __init__(self, cfg: BaseTokenSearcherConfig) -> None:
        super().__init__(cfg)
        self.cfg = cfg #################################################


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
        self, input_data: Union[InputWithThreshold, Dict[str, Any]]
    ) -> InputWithThreshold:
        input_data = super()._preprocess(input_data)
        input_data.threshold = self.choose_threshold(input_data)
        return input_data


    @abstractmethod
    def _process(
        self, input_data: InputWithThreshold
    ) -> Any:
        pass


    @abstractmethod
    def _postprocess(
        self, 
        input_data: InputWithThreshold, 
        predicts: Any
    ) -> BaseTokenSearcherOutput:
        pass


    def execute(
        self, 
        input_data: Union[InputWithThreshold, Dict[str, Any]]
    ) -> BaseTokenSearcherOutput:
        input_data = self._preprocess(input_data)
        return self._postprocess(
            input_data,
            self._process(input_data)
        )