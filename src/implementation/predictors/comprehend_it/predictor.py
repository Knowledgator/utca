from typing import Any, Type

from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipeline
)
from implementation.predictors.comprehend_it.schema import (
    ComprehendItPredictorConfig,
    ComprehendItPredictorInput, 
    ComprehendItPredictorOutput,
    ComprehendItPredictorConfigType, 
    ComprehendItPredictorInputType, 
    ComprehendItPredictorOutputType
)   

class ComprehendItPredictor(
    TransformersPipeline[
        ComprehendItPredictorConfigType,
        ComprehendItPredictorInputType, 
        ComprehendItPredictorOutputType
    ]
):
    def __init__(
        self, 
        cfg: ComprehendItPredictorConfigType=ComprehendItPredictorConfig(),
        input_class: Type[ComprehendItPredictorInputType]=ComprehendItPredictorInput,
        output_class: Type[ComprehendItPredictorOutputType]=ComprehendItPredictorOutput
    ) -> None:
        super().__init__(
            cfg,
            input_class,
            output_class
        )

    
    def get_predictions(self, **inputs: Any) -> Any:
        return self.pipeline( # type: ignore
            inputs.pop("text"), inputs.pop("labels"), **inputs
        )