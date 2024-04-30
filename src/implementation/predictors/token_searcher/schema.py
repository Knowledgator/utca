from typing import Any, Dict, List, Union, Optional

from transformers import ( # type: ignore
    PreTrainedModel,
    TFPreTrainedModel,
    # PreTrainedTokenizer,
)

from implementation.predictors.transformers.transformers_pipeline import (
    TransformersPipelineConfig
)
from implementation.predictors.transformers.schema import (
    TransformersBasicInput,
    TransformersBasicOutput
)

class TokenSearcherPredictorConfig(TransformersPipelineConfig):
    """
    Prebuild configuration that describes default parameters for 
    knowledgator/UTC models pipeline.
    """
    task: Optional[str]="ner"
    """
    Transformers pipeline task
    """
    model: Optional[Union[
        str,
        PreTrainedModel,
        TFPreTrainedModel
    ]]="knowledgator/UTC-DeBERTa-small"
    kwargs: Optional[Dict[str, Any]]={
        "aggregation_strategy": "first",
        "batch_size": 12
    }
    """
    Extra parameters
    """


class TokenSearcherPredictorInput(TransformersBasicInput):
    inputs: List[str]
    """
    Text inputs
    """


class TokenSearcherPredictorOutput(TransformersBasicOutput):
    output: List[List[Dict[str, Any]]]
    """
    Entities of corresponding inputs
    """