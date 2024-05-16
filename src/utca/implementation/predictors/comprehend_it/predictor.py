from typing import Optional, Type

from utca.core.executable_level_1.schema import Input, Output
from utca.implementation.predictors.transformers_predictor.transformers_pipeline import (
    TransformersPipeline
)
from utca.implementation.predictors.transformers_predictor.transformers_pipeline import (
    TransformersPipelineConfig
)
from utca.implementation.predictors.comprehend_it.schema import (
    ComprehendItPredictorConfig,
    ComprehendItPredictorInput,
    ComprehendItPredictorOutput
)   

class ComprehendItPredictor(
    TransformersPipeline[Input, Output]
):
    """
    Predictor for text classifications models
    """
    def __init__(
        self, 
        cfg: Optional[TransformersPipelineConfig]=None,
        input_class: Type[Input]=ComprehendItPredictorInput,
        output_class: Type[Output]=ComprehendItPredictorOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            cfg (Optional[TransformersPipelineConfig], optional): Configuration for predictor.
                If value equals to None, default ComprehendItPredictorConfig configuration will be used.
                Defaults to None.

            input_class (Type[Input], optional): Class for input validation.
                Defaults to ComprehendItPredictorInput.
            
            output_class (Type[Output], optional): Class for output validation.
                Defaults to ComprehendItPredictorOutput.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(
            cfg=cfg or ComprehendItPredictorConfig(),
            input_class=input_class,
            output_class=output_class,
            name=name,
        )