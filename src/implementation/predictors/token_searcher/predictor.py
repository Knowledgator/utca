from typing import Type

from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipeline
)
from implementation.predictors.token_searcher.schema import (
    TokenSearcherPredictorConfig, 
    TokenSearcherPredictorInput, 
    TokenSearcherPredictorOutput,
    TokenSearcherPredictorConfigType, 
    TokenSearcherPredictorInputType, 
    TokenSearcherPredictorOutputType
)   

class TokenSearcherPredictor(
    TransformersPipeline[
        TokenSearcherPredictorConfigType,
        TokenSearcherPredictorInputType, 
        TokenSearcherPredictorOutputType
    ]
):
    def __init__(
        self, 
        cfg: TokenSearcherPredictorConfigType=TokenSearcherPredictorConfig(),
        input_class: Type[TokenSearcherPredictorInputType]=TokenSearcherPredictorInput,
        output_class: Type[TokenSearcherPredictorOutputType]=TokenSearcherPredictorOutput
    ) -> None:
        super().__init__(
            cfg,
            input_class,
            output_class
        )