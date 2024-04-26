from typing import Any, Dict, List, TypeVar, Union, Optional

from transformers import ( # type: ignore
    PreTrainedModel,
    TFPreTrainedModel,
)

from core.executable_level_1.schema import IOModel
from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipelineConfig
)

class ComprehendItPredictorConfig(TransformersPipelineConfig):
    """
    Comprehend-it configuration
    """
    task: Optional[str]="zero-shot-classification"
    """
    Transformers pipeline task
    """
    model: Optional[Union[
        str,
        PreTrainedModel,
        TFPreTrainedModel
    ]]="knowledgator/comprehend_it-base"
    """
    Model
    """
    kwargs: Optional[Dict[str, Any]]={
        "batch_size": 8
    }
    """
    Extra arguments
    """


class ComprehendItPredictorInput(IOModel):
    text: str
    """
    Text to classify
    """
    labels: List[str]
    """
    Classification labels to use
    """


class ComprehendItPredictorOutput(IOModel):
    sequence: str
    """
    Text used for classification
    """
    labels: List[str]
    """
    Classified labels
    """
    scores: List[float]
    """
    Classification scores
    """


ComprehendItPredictorConfigType = TypeVar("ComprehendItPredictorConfigType", bound=ComprehendItPredictorConfig)
ComprehendItPredictorInputType = TypeVar("ComprehendItPredictorInputType", bound=ComprehendItPredictorInput)
ComprehendItPredictorOutputType = TypeVar("ComprehendItPredictorOutputType", bound=ComprehendItPredictorOutput)