from __future__ import annotations
from typing import TypeVar

from core.executable_level_1.schema import Input, Output, Config

PredictorConfigType = TypeVar('PredictorConfigType', bound=Config, contravariant=True)
PredictorInputType = TypeVar('PredictorInputType', bound=Input)
PredictorOutputType = TypeVar('PredictorOutputType', bound=Output)