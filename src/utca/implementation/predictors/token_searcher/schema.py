from typing import Any, Dict, List, Union, Optional

from transformers import ( # type: ignore
    PreTrainedModel,
    TFPreTrainedModel,
)

from utca.implementation.predictors.transformers_predictor.transformers_pipeline import (
    TransformersPipelineConfig
)
from utca.implementation.predictors.transformers_predictor.schema import (
    TransformersBasicInput,
    TransformersBasicOutput
)
from utca.implementation.predictors.token_searcher.token_searcher_pipeline import (
    TokenClassificationPipeline
)

class TokenSearcherPredictorConfig(TransformersPipelineConfig):
    """
    Prebuild configuration that describes default parameters for 
    knowledgator/UTC models pipeline.
    """
    task: Optional[str]="ner"
    model: Optional[Union[
        str,
        PreTrainedModel,
        TFPreTrainedModel
    ]]="knowledgator/UTC-DeBERTa-small"
    pipeline_class: Optional[Any]=TokenClassificationPipeline
    kwargs: Optional[Dict[str, Any]]={
        "aggregation_strategy": "first",
        "batch_size": 12
    }


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