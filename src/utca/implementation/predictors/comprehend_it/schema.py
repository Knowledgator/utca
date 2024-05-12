from typing import Any, Dict, List, Union, Optional

from transformers import ( # type: ignore
    PreTrainedModel,
    TFPreTrainedModel,
)

from utca.core.executable_level_1.schema import IOModel
from utca.implementation.predictors.transformers_predictor.transformers_pipeline import (
    TransformersPipelineConfig
)

class ComprehendItPredictorConfig(TransformersPipelineConfig):
    """
    Prebuild configuration that describes default parameters for knowledgator/comprehend_it 
    models pipeline
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
    kwargs: Optional[Dict[str, Any]]={
        "batch_size": 8
    }
    """
    Extra arguments
    """


class ComprehendItPredictorInput(IOModel):
    """
    Arguments:
        sequences (str): Text to classify.

        candidate_labels (List[str]): Classification labels to use.
    """
    sequences: str
    candidate_labels: List[str]


class ComprehendItPredictorOutput(IOModel):
    """
    Arguments:
        sequence (str): Text used for classification.

        labels (List[str]): Classified labels.

        scores (List[float]): Classification scores.
    """
    sequence: str
    labels: List[str]
    scores: List[float]