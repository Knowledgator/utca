from typing import Optional, Type

from utca.core.executable_level_1.schema import Input, Output
from utca.implementation.predictors.transformers_predictor.transformers_pipeline import (
    TransformersPipeline,
    TransformersPipelineConfig
)
from utca.implementation.predictors.token_searcher.schema import (
    TokenSearcherPredictorConfig, 
    TokenSearcherPredictorInput, 
    TokenSearcherPredictorOutput
)   

class TokenSearcherPredictor(
    TransformersPipeline[Input, Output]
):
    """
    TokenSearcher predictor. This predictor is specifically build for knowledgator/UTC models. 
    For more details about models, see:
    https://huggingface.co/collections/knowledgator/universal-token-classification-65a3a5d3f266d20b2e05c34d
    """
    def __init__(
        self, 
        cfg: Optional[TransformersPipelineConfig]=None,
        input_class: Type[Input]=TokenSearcherPredictorInput,
        output_class: Type[Output]=TokenSearcherPredictorOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            cfg (TransformersPipelineConfig, optional): Configuration for predictor.
                If value equals to None, default TokenSearcherPredictorConfig configuration
                will be used. Defaults to None.
            
            input_class (Type[Input], optional): Class for input validation.
                Defaults to TokenSearcherPredictorInput.
            
            output_class (Type[Output], optional): Class for output validation.
                Defaults to TokenSearcherPredictorOutput.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(
            cfg=cfg or TokenSearcherPredictorConfig(),
            input_class=input_class,
            output_class=output_class,
            name=name,
        )