from typing import Any, Type

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
    def __init__(
        self, 
        cfg: ComprehendItPredictorConfig=ComprehendItPredictorConfig(),
        input_class: Type[ComprehendItPredictorInputType]=ComprehendItPredictorInput,
        output_class: Type[ComprehendItPredictorOutputType]=ComprehendItPredictorOutput
    ) -> None:
        super().__init__(
            cfg,
            input_class,
            output_class
        )

    
    def invoke(self, input_data: ComprehendItPredictorInputType) -> Any:
        inputs = input_data.model_dump()
        return self.pipeline( # type: ignore
            inputs.pop("text"), inputs.pop("labels"), **inputs
        )