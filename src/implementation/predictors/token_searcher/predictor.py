from typing import Optional, Type

from core.executable_level_1.schema import Input, Output
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipeline
)
from implementation.predictors.token_searcher.schema import (
    TokenSearcherPredictorConfig, 
    TokenSearcherPredictorInput, 
    TokenSearcherPredictorOutput
)   

class TokenSearcherPredictor(
    TransformersPipeline[Input, Output]
):
    def __init__(
        self, 
        cfg: TokenSearcherPredictorConfig=TokenSearcherPredictorConfig(),
        input_class: Type[Input]=TokenSearcherPredictorInput,
        output_class: Type[Output]=TokenSearcherPredictorOutput,
        name: Optional[str]=None,
    ) -> None:
        super().__init__(
            cfg=cfg,
            input_class=input_class,
            output_class=output_class,
            name=name,
        )