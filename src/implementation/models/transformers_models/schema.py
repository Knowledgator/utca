from typing import TypeVar

from core.model_level_2.schema import Config

class TransformersModelConfig(Config):
    model: str
    sents_batch: int=10
    batch_size: int=12
    device: str='cpu'


TransformersModelConfigType = TypeVar(
    'TransformersModelConfigType', 
    bound=TransformersModelConfig, 
    contravariant=True
)