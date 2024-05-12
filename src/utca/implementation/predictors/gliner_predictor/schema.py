import torch
from typing import Any, Dict, List, Union, Optional

from utca.core.executable_level_1.schema import IOModel, Config


class GLiNERPredictorConfig(Config):
    """
    Prebuild configuration that describes default parameters for 
    GLiNER models pipeline.
    """
    model_name: str = "urchade/gliner_small-v2.1"
    device: str= "cpu"

class GLiNERPredictorInput(IOModel):
    texts: List[str]
    labels: List[str]
    threshold: float = 0.5

    """
    GLiNER inputs
    """


class GLiNERPredictorOutput(IOModel):
    output: List[List[Dict[str, Any]]]
    """
    Entities of corresponding inputs
    """