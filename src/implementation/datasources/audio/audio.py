from typing import Optional

from core.datasource_level_2.datasource import DatasourceManager
from core.datasource_level_2.schema import (
    DatasourceConfig,
)
from implementation.datasources.audio.schema import (
    AudioReadInput,
    AudioReadOutput,
    AudioWriteInput,
    AudioWriteOutput
)
from implementation.datasources.audio.actions import (
    AudioRead,
    AudioWrite
)


class Audio(DatasourceManager[
    DatasourceConfig,
    AudioReadInput,
    AudioReadOutput,

    DatasourceConfig,
    AudioWriteInput,
    AudioWriteOutput,
]):
    def read(
        self, cfg: Optional[DatasourceConfig]=None,
    ) -> AudioRead:
        return AudioRead(cfg)

    
    def write(
        self, cfg: Optional[DatasourceConfig]=None,
    ) -> AudioWrite:
        return AudioWrite(cfg)