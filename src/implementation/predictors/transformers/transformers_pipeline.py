from typing import TypeVar, Any, Type, Union, Optional, Dict

import torch
from transformers import ( # type: ignore
    pipeline, # type: ignore
    Pipeline,
    PreTrainedModel,
    TFPreTrainedModel,
    PretrainedConfig,
    PreTrainedTokenizer,
)
from transformers.image_processing_utils import ( # type: ignore
    BaseImageProcessor
)

from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.schema import (
    Config, Input, InputType, OutputType
)
from core.predictor_level_2.predictor import Predictor

class TransformersPipelineConfig(Config):
    class Config:
        arbitrary_types_allowed = True
        protected_namespaces = ()

    task: Optional[str]=None
    model: Optional[Union[
        str,
        PreTrainedModel,
        TFPreTrainedModel
    ]]=None
    config: Optional[Union[
        str,
        PretrainedConfig
    ]]=None
    tokenizer: Optional[Union[
        str,
        PreTrainedTokenizer
    ]]=None
    feature_extractor: Optional[Any]=None
    image_processor: Optional[Union[
        str, 
        BaseImageProcessor
    ]]=None
    framework: Optional[str]=None
    revision: Optional[str]=None
    use_fast: bool=True
    token: Optional[Union[str, bool]]=None
    device: Optional[Union[int, str, torch.device]]=None
    device_map: Optional[Union[
        str, 
        Dict[str, Union[int, str, torch.device]
    ]]]=None
    torch_dtype: Optional[Union[str, torch.dtype]]=None
    trust_remote_code: Optional[bool]=None
    model_kwargs: Optional[Dict[str, Any]]=None
    pipeline_class: Optional[Any]=None
    kwargs: Optional[Dict[str, Any]]=None


    @property
    def pipeline_config(self) -> Dict[str, Any]:
        tmp = self.model_dump(exclude={"kwargs"})
        if self.kwargs:
            tmp.update(self.kwargs)
        return tmp


TransformersPipelineConfigType = TypeVar(
    'TransformersPipelineConfigType', 
    bound=TransformersPipelineConfig
)

class TransformersPipeline(
    Predictor[InputType, OutputType]
):  
    pipeline: Pipeline

    def __init__(
        self,
        cfg: TransformersPipelineConfig,
        input_class: Type[InputType],
        output_class: Type[OutputType],
    ) -> None:
        self.pipeline: Pipeline = pipeline(
            **cfg.pipeline_config
        )
        super().__init__(input_class, output_class)


    def invoke(self, input_data: InputType, evaluator: Evaluator) -> Any:
        inputs = input_data.model_dump()
        return self.ensure_dict(self.pipeline(**inputs)) # type: ignore
    

    @property
    def config(self) -> Any:
        return self.pipeline.model.config # type: ignore


class SummarizationInput(Input):
    inputs: Any

SummarizationInputType = TypeVar(
    "SummarizationInputType",
    bound=SummarizationInput
)

class TransformersSummarizationPipeline(
    TransformersPipeline[
        SummarizationInputType, 
        OutputType
    ]
):
    def invoke(self, input_data: SummarizationInputType, evaluator: Evaluator) -> Any:
        inputs = input_data.model_dump()
        return self.ensure_dict(
            self.pipeline( # type: ignore
                inputs.pop("inputs"), **inputs
            )
        )