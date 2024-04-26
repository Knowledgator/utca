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
    """
    TokenSearcher predictor
    """
    def __init__(
        self, 
        cfg: Optional[TokenSearcherPredictorConfig]=None,
        input_class: Type[Input]=TokenSearcherPredictorInput,
        output_class: Type[Output]=TokenSearcherPredictorOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            cfg (TokenSearcherPredictorConfig, optional): Configuration for predictor.
                If value equals to None, default configuration will be used. Defaults to None.
            
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