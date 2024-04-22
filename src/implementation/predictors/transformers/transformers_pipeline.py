from typing import TypeVar, Any, Type, Union, Optional, Dict

from pydantic import ConfigDict
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
    Config, IOModel, Input, Output
)
from core.predictor_level_2.predictor import Predictor
from implementation.predictors.transformers.utils import ensure_dict

class TransformersPipelineConfig(Config):
    model_config = ConfigDict(
        arbitrary_types_allowed=True, 
        protected_namespaces=()
    )

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
    Predictor[Input, Output]
):  
    pipeline: Pipeline

    def __init__(
        self,
        cfg: TransformersPipelineConfig,
        input_class: Type[Input],
        output_class: Type[Output],
        name: Optional[str]=None,
    ) -> None:
        self.pipeline: Pipeline = pipeline(
            **cfg.pipeline_config
        )
        super().__init__(
            input_class=input_class, 
            output_class=output_class, 
            name=name,
        )


    def invoke(self, input_data: Input, evaluator: Evaluator) -> Dict[str, Any]:
        inputs = input_data.extract()
        return ensure_dict(self.pipeline(**inputs)) # type: ignore
    

    @property
    def config(self) -> Any:
        return self.pipeline.model.config # type: ignore


class SummarizationInput(IOModel):
    inputs: Any

SummarizationInputType = TypeVar(
    "SummarizationInputType",
    bound=SummarizationInput
)

class TransformersSummarizationPipeline(
    TransformersPipeline[
        SummarizationInputType, 
        Output
    ]
):
    def invoke(self, input_data: SummarizationInputType, evaluator: Evaluator) -> Dict[str, Any]:
        inputs = input_data.extract()
        return ensure_dict(self.pipeline( # type: ignore
            inputs.pop("inputs"), **inputs
        ))