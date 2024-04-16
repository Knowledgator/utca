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
    def __init__(
        self, 
        cfg: ComprehendItPredictorConfig=ComprehendItPredictorConfig(),
        input_class: Type[ComprehendItPredictorInputType]=ComprehendItPredictorInput,
        output_class: Type[ComprehendItPredictorOutputType]=ComprehendItPredictorOutput,
        name: Optional[str]=None,
    ) -> None:
        super().__init__(
            cfg=cfg,
            input_class=input_class,
            output_class=output_class,
            name=name,
        )

    
    def invoke(self, input_data: ComprehendItPredictorInputType, evaluator: Evaluator) -> Dict[str, Any]:
        inputs = input_data.model_dump()
        return self.pipeline( # type: ignore
            inputs.pop("text"), inputs.pop("labels"), **inputs
        )