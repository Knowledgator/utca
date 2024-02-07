from typing import Generic
from abc import ABC, abstractmethod

from core.executable_level_1.executable import Executable
from core.datasource_level_2.schema import (
    DatasourceInputType, 
    DatasourceOutputType, 
    DatasourceConfigType,
    ReadConfig,
    ReadInput,
    ReadOutput,
    WriteConfig,
    WriteInput,
    WriteOutput,
)

class DatasourceAction(Executable[DatasourceConfigType, DatasourceInputType, DatasourceOutputType]):
    ...


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