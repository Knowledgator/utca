from typing import Optional, List, Union, Type

from core.executable_level_1.actions import (
    OneToOne, OneToMany, ManyToOne, ManyToMany
)
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.task import NERTask
from core.task_level_3.schema import (
    InputWithThreshold, 
    NEROutput,
    NERConfig 
)
from core.task_level_3.objects.objects import (
    ClassifiedEntity
)
from implementation.predictors.token_searcher.predictor import (
    TokenSearcherPredictor
)
from implementation.predictors.token_searcher.schema import (
    TokenSearcherPredictorConfig, 
    TokenSearcherPredictorInput, 
    TokenSearcherPredictorOutput
)
from implementation.tasks.text_processing.ner.token_searcher.actions import (
    TokenSearcherNERPreprocessor,
    TokenSearcherNERPostprocessor
)

class TokenSearcherNERInput(InputWithThreshold):
    text: str
    labels: list[str]


class TokenSearcherNEROutput(NEROutput[ClassifiedEntity]):
    text: str


class TokenSearcherNERTask(
    NERTask[
        NERConfig,
        TokenSearcherNERInput, 
        TokenSearcherNEROutput
    ]
):
    def __init__(
        self,
        cfg: Optional[NERConfig]=None, 
        predictor: Optional[Predictor[
            TokenSearcherPredictorConfig, 
            TokenSearcherPredictorInput, 
            TokenSearcherPredictorOutput
        ]]=None,
        preprocess: Optional[List[Union[OneToOne, OneToMany, ManyToOne, ManyToMany]]]=None,
        postprocess: Optional[List[Union[OneToOne, OneToMany, ManyToOne, ManyToMany]]]=None,
        input_class: Type[TokenSearcherNERInput]=TokenSearcherNERInput,
        output_class: Type[TokenSearcherNEROutput]=TokenSearcherNEROutput
    ) -> None:
        self.cfg = cfg or NERConfig()
        self.predictor = predictor or TokenSearcherPredictor()
        self._preprocess = preprocess or [TokenSearcherNERPreprocessor()],
        self._postprocess = postprocess or [TokenSearcherNERPostprocessor()],
        self.input_class = input_class
        self.output_class = output_class