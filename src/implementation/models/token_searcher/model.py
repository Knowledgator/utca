from transformers import ( # type: ignore
    pipeline, AutoTokenizer, AutoModelForTokenClassification # type: ignore
) 
from pydantic import BaseModel

from src.model_level_2.model import Model, ModelConfigs
from src.model_level_2.schema import Prompt

class Entity(BaseModel):
    entity_group: str 
    score: float
    word: str
    start: int
    end: int


class TokenSearcherOutputs(BaseModel):
    outputs: list[list[Entity]]


class TokenSearcherConfigs(ModelConfigs):
    model_name: str
    device: str='cpu'
    batch_size: int=12


class TokenSearcher(Model[Prompt, TokenSearcherOutputs]):
    def __init__(self, cfg: TokenSearcherConfigs) -> None:
        super().__init__(cfg)

        tokenizer = AutoTokenizer.from_pretrained(cfg.model_name) # type: ignore
        model = AutoModelForTokenClassification.from_pretrained(cfg.model_name) # type: ignore

        try:
            self.pipeline = pipeline(
                "ner", 
                model=model, # type: ignore
                tokenizer=tokenizer,
                aggregation_strategy='first', 
                batch_size=cfg.batch_size, # TODO: check what it actually does!
                device=cfg.device
            )
        except Exception as e:
            raise ValueError(e)

    
    def invoke(self, input_data: Prompt) -> TokenSearcherOutputs:
        return TokenSearcherOutputs.parse_obj({
            'outputs': self.pipeline([input_data.prompt])
        })