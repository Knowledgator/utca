from __future__ import annotations
from typing import TypeVar

from core.executable_level_1.schema import Input, Output, Config

class DatasourceConfig(Config):
    ...


class DatasourceInput(Input):
    ...
    

class DatasourceOutput(Output):
    ...

DatasourceConfigType = TypeVar('DatasourceConfigType', bound=DatasourceConfig, contravariant=True)
DatasourceInputType = TypeVar('DatasourceInputType', bound=DatasourceInput)
DatasourceDataType = TypeVar('DatasourceDataType', bound=DatasourceOutput)