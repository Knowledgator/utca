from typing import Any, Dict, List

from pydantic import ConfigDict

from utca.core.executable_level_1.schema import IOModel, Config

class GLiNERPredictorConfig(Config):
    """
    Prebuild configuration that describes default parameters for 
    GLiNER models pipeline.
    """
    model_config = ConfigDict(protected_namespaces=())

    model_name: str = "urchade/gliner_small-v2.1"
    device: str= "cpu"


class GLiNERPredictorInput(IOModel):
    """
    GLiNER inputs
    """
    texts: List[str]
    labels: List[str]
    threshold: float = 0.5



class GLiNERPredictorOutput(IOModel):
    """
    Entities of corresponding inputs
    """
    output: List[List[Dict[str, Any]]]