from typing import TypeVar

from core.executable_level_1.schema import Config

class TransformersModelConfig(Config):
    model: str
    batch_size: int=12
    device: str='cpu'


TransformersModelConfigType = TypeVar(
    'TransformersModelConfigType', 
    bound=TransformersModelConfig, 
    contravariant=True
)