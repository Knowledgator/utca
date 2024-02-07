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
DatasourceOutputType = TypeVar('DatasourceOutputType', bound=DatasourceOutput)

ReadConfig = TypeVar('ReadConfig', bound=DatasourceConfig, contravariant=True)
ReadInput = TypeVar('ReadInput', bound=DatasourceInput)
ReadOutput = TypeVar('ReadOutput', bound=DatasourceOutput)

WriteConfig = TypeVar('WriteConfig', bound=DatasourceConfig, contravariant=True)
WriteInput = TypeVar('WriteInput', bound=DatasourceInput)
WriteOutput = TypeVar('WriteOutput', bound=DatasourceOutput)