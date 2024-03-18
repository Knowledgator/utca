from typing import Any, Dict, List, TypeVar, Union, Optional

from transformers import ( # type: ignore
    PreTrainedModel,
    TFPreTrainedModel,
)

from core.executable_level_1.schema import (
    Input, Output
)
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipelineConfig
)

class ComprehendItPredictorConfig(TransformersPipelineConfig):
    task: Optional[str]="zero-shot-classification"
    model: Optional[Union[
        str,
        PreTrainedModel,
        TFPreTrainedModel
    ]]="knowledgator/comprehend_it-base"
    kwargs: Optional[Dict[str, Any]]={
        "batch_size": 8
    }


class ComprehendItPredictorInput(Input):
    text: str
    labels: List[str]


class ComprehendItPredictorOutput(Output):
    sequence: str
    labels: List[str]
    scores: List[float]


ComprehendItPredictorConfigType = TypeVar("ComprehendItPredictorConfigType", bound=ComprehendItPredictorConfig)
ComprehendItPredictorInputType = TypeVar("ComprehendItPredictorInputType", bound=ComprehendItPredictorInput)
ComprehendItPredictorOutputType = TypeVar("ComprehendItPredictorOutputType", bound=ComprehendItPredictorOutput)