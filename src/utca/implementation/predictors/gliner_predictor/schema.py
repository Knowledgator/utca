from typing import Any, Dict, List

from pydantic import ConfigDict

from utca.core.executable_level_1.schema import IOModel, Config

class GLiNERPredictorConfig(Config):
    """
    Prebuild configuration that describes default parameters for 
    GLiNER models pipeline.
    
    - model_name (str): Identifier of the model to load. Defaults to `urchade/gliner_small-v2.1`.
        - Either the `model_id` of a model hosted on the Hub, e.g. `urchade/gliner_small-v2.1`.
        - Or a local path to a `directory` containing model weights saved using
            [`~transformers.PreTrainedModel.save_pretrained`], e.g., `../path/to/my_model_directory/`.
    - local_files_only (bool): Use only local files, don't download. Defaults to False.
    - load_tokenizer (bool): Whether to load the tokenizer. Defaults to False.
    - load_onnx_model (bool): Load ONNX version of the model. Defaults to False.
    - onnx_model_file (str): Filename for ONNX model. Defaults to `model.onnx`.
    - device (str): Device to map model to. Defaults to `cpu`.
    """
    model_config = ConfigDict(protected_namespaces=())

    model_name: str = "urchade/gliner_small-v2.1"
    local_files_only: bool = False
    load_tokenizer: bool = False
    load_onnx_model: bool = False
    onnx_model_file: str = "model.onnx"
    device: str = "cpu"


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