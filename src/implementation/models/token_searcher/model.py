from typing import Dict, Type, Any

from implementation.models.transformers_models.model import (
    TransformersModel
)
from implementation.models.token_searcher.schema import (
    TokenSearcherModelConfig, 
    TokenSearcherModelInput, 
    TokenSearcherModelOutput
)   

class TokenSearcherModel(
    TransformersModel[
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