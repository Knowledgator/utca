from typing import Generic, TypeVar
from abc import ABC, abstractmethod

from core.executable_level_1.executable import Executable
from core.datasource_level.schema import (
    DatasourceInput, 
    DatasourceOutput, 
    DatasourceConfig,
    DatasourceInputType, 
    DatasourceDataType, 
    DatasourceConfigType
)

class DatasourceAction(Executable[DatasourceConfigType, DatasourceInputType, DatasourceDataType]):
    ...


ReadConfig = TypeVar('ReadConfig', bound=DatasourceConfig)
ReadInput = TypeVar('ReadInput', bound=DatasourceInput)
ReadOutput = TypeVar('ReadOutput', bound=DatasourceOutput)

WriteConfig = TypeVar('WriteConfig', bound=DatasourceConfig)
WriteInput = TypeVar('WriteInput', bound=DatasourceInput)
WriteOutput = TypeVar('WriteOutput', bound=DatasourceOutput)

CreateConfig = TypeVar('CreateConfig', bound=DatasourceConfig)
CreateInput = TypeVar('CreateInput', bound=DatasourceInput)
CreateOutput = TypeVar('CreateOutput', bound=DatasourceOutput)


class DatasourceManager(
    Generic[
        ReadConfig,
        ReadInput,
        ReadOutput,

        WriteConfig,
        WriteInput,
        WriteOutput,

        CreateConfig,
        CreateInput,
        CreateOutput,
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


    @abstractmethod
    def create(
        self, cfg: CreateConfig,
    ) -> DatasourceAction[
        CreateConfig,
        CreateInput,
        CreateOutput,
    ]:
        ...