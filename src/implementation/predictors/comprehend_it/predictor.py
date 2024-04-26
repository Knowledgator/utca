from typing import Any, Dict, Optional, Type

from core.executable_level_1.interpreter import Evaluator
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipeline
)
from implementation.predictors.comprehend_it.schema import (
    ComprehendItPredictorConfig,
    ComprehendItPredictorInput, 
    ComprehendItPredictorOutput,
    ComprehendItPredictorInputType, 
    ComprehendItPredictorOutputType
)   

class ComprehendItPredictor(
    TransformersPipeline[
        ComprehendItPredictorInputType,
        ComprehendItPredictorOutputType
    ]
):
    """
    Predictor for text classifications models
    """
    def __init__(
        self, 
        cfg: Optional[ComprehendItPredictorConfig]=None,
        input_class: Type[ComprehendItPredictorInputType]=ComprehendItPredictorInput,
        output_class: Type[ComprehendItPredictorOutputType]=ComprehendItPredictorOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            cfg (Optional[ComprehendItPredictorConfig], optional): Configuration for predictor.
                If value equals to None, default configuration will be used. Defaults to None.

            input_class (Type[ComprehendItPredictorInputType], optional): Class for input validation.
                Defaults to ComprehendItPredictorInput.
            
            output_class (Type[ComprehendItPredictorOutputType], optional): Class for output validation.
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

    
    def invoke(self, input_data: ComprehendItPredictorInputType, evaluator: Evaluator) -> Dict[str, Any]:
        inputs = input_data.extract()
        return self.pipeline( # type: ignore
            inputs.pop("text"), inputs.pop("labels"), **inputs
        )