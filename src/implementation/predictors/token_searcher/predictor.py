from typing import Dict, Type, Any, Optional, List

from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipeline
)
from implementation.predictors.token_searcher.schema import (
    TokenSearcherPredictorConfig, 
    TokenSearcherPredictorInput, 
    TokenSearcherPredictorOutput
)   

class TokenSearcherPredictor(
    TransformersPipeline[
        TokenSearcherPredictorConfig,
        TokenSearcherPredictorInput, 
        TokenSearcherPredictorOutput
    ]
):
    def __init__(
        self, 
        cfg: Optional[TokenSearcherPredictorConfig]=None,
        input_class: Type[TokenSearcherPredictorInput]=TokenSearcherPredictorInput,
        output_class: Type[TokenSearcherPredictorOutput]=TokenSearcherPredictorOutput
    ) -> None:
        super().__init__(
            cfg or TokenSearcherPredictorConfig(),
            input_class,
            output_class
        )


    def invoke(
        self, input_data: TokenSearcherPredictorInput
    ) -> Dict[str, Any]:
        return {
            'inputs': input_data.inputs,
            'outputs': self.get_predictions(**input_data.model_dump())
        }
    

    def invoke_batch(
        self, input_data: List[TokenSearcherPredictorInput]
    ) -> List[Dict[str, Any]]:
        raise Exception('TODO!')