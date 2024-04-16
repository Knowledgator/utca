from typing import Optional, Type

from core.executable_level_1.schema import InputType, OutputType
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipeline
)
from implementation.predictors.token_searcher.schema import (
    TokenSearcherPredictorConfig, 
    TokenSearcherPredictorInput, 
    TokenSearcherPredictorOutput
)   

class TokenSearcherPredictor(
    TransformersPipeline[InputType, OutputType]
):
    def __init__(
        self, 
        cfg: TokenSearcherPredictorConfig=TokenSearcherPredictorConfig(),
        input_class: Type[InputType]=TokenSearcherPredictorInput,
        output_class: Type[OutputType]=TokenSearcherPredictorOutput,
        name: Optional[str]=None,
    ) -> None:
        super().__init__(
            cfg=cfg,
            input_class=input_class,
            output_class=output_class,
            name=name,
        )