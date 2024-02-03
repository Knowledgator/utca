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
    input_class: Type[TokenSearcherModelInput] = TokenSearcherModelInput
    output_class: Type[TokenSearcherModelOutput] = TokenSearcherModelOutput

    def invoke(
        self, input_data: TokenSearcherModelInput
    ) -> Dict[str, Any]:
        return {
            'inputs': input_data.inputs,
            'outputs': self.get_predictions(input_data.inputs)
        }