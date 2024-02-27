from __future__ import annotations
from typing import TypeVar, Any

from core.executable_level_1.schema import Input, Output, Config

class PredictorInput(Input):
    inputs: Any

class PredictorOutput(Output):
    outputs: Any

PredictorConfigType = TypeVar('PredictorConfigType', bound=Config, contravariant=True)
PredictorInputType = TypeVar('PredictorInputType', bound=PredictorInput)
PredictorOutputType = TypeVar('PredictorOutputType', bound=PredictorOutput)