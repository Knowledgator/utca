from typing import Type, Any

from transformers import ( # type: ignore
    pipeline # type: ignore
)

from core.executable_level_1.schema import InputType, OutputType
from core.model_level_2.model import Model
from core.model_level_2.transformers_models.schema import (
    TransformersPipelineConfigType
)

class TransformersPipeline(
    Model[
        TransformersPipelineConfigType, 
        InputType, 
        OutputType
    ]
):
    input_data_type: Type[InputType]
    
    def __init__(self, cfg: TransformersPipelineConfigType) -> None:        
        pipeline_parameters = cfg.model_dump()
        pipeline_parameters.pop('name')
        self.pipeline = cfg.pipeline 
        super().__init__(cfg)


    def get_predictions(
        self, inputs: Any
    ) -> Any:
        return self.pipeline(inputs) # type: ignore