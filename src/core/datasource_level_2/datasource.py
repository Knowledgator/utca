from typing import Generic, TypeVar
from abc import ABC, abstractmethod

from core.executable_level_1.executable import Executable
from core.datasource_level_2.schema import (
    DatasourceInput, 
    DatasourceOutput, 
    DatasourceConfig,
    DatasourceInputType, 
    DatasourceOutputType, 
    DatasourceConfigType
)

class DatasourceAction(Executable[DatasourceConfigType, DatasourceInputType, DatasourceOutputType]):
    ...


ReadConfig = TypeVar('ReadConfig', bound=DatasourceConfig)
ReadInput = TypeVar('ReadInput', bound=DatasourceInput)
ReadOutput = TypeVar('ReadOutput', bound=DatasourceOutput)

WriteConfig = TypeVar('WriteConfig', bound=DatasourceConfig)
WriteInput = TypeVar('WriteInput', bound=DatasourceInput)
WriteOutput = TypeVar('WriteOutput', bound=DatasourceOutput)


class DatasourceManager(
    Generic[
        ReadConfig,
        ReadInput,
        ReadOutput,

        WriteConfig,
        WriteInput,
        WriteOutput,
    ],
    ABC
):
    @abstractmethod
    def read(
        self, cfg: ReadConfig,
    ) -> DatasourceAction[
        ReadConfig,
        ReadInput,
        ReadOutput,
    ]:
        ...

    
    @abstractmethod
    def write(
        self, cfg: WriteConfig,
    ) -> DatasourceAction[
        WriteConfig,
        WriteInput,
        WriteOutput,
    ]:
        ...