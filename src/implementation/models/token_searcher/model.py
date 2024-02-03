from typing import Dict, Type, Any

from core.model_level_2.model import PromptModel
from core.model_level_2.transformers_models.pipeline import (
    TransformersPipeline
)
from implementation.models.token_searcher.schema import (
    TokenSearcherModelConfig, 
    TokenSearcherModelInput, 
    TokenSearcherModelOutput
)   

class TokenSearcherModel(
    TransformersPipeline[
        TokenSearcherModelConfig, 
        TokenSearcherModelInput, 
        TokenSearcherModelOutput
    ],
    PromptModel[
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