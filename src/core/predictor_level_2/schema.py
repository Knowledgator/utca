from __future__ import annotations
from typing import TypeVar

from core.executable_level_1.schema import Input, Output, Config

class PredictorConfig(Config):
    ...


class PredictorInput(Input):
    ...


class PredictorOutput(Output):
    ...

PredictorConfigType = TypeVar('PredictorConfigType', bound=PredictorConfig)
PredictorInputType = TypeVar('PredictorInputType', bound=PredictorInput)
PredictorOutputType = TypeVar('PredictorOutputType', bound=PredictorOutput)