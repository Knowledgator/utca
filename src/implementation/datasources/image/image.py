from typing import Optional

from core.datasource_level_2.datasource import DatasourceManager
from core.datasource_level_2.schema import (
    DatasourceConfig
)
from implementation.datasources.image.schema import (
    ImageReadInput,
    ImageReadOutput,
    ImageWriteInput,
    ImageWriteOutput
)
from implementation.datasources.image.actions import (
    ImageRead,
    ImageWrite
)


class Image(DatasourceManager[
    DatasourceConfig,
    ImageReadInput,
    ImageReadOutput,

    DatasourceConfig,
    ImageWriteInput,
    ImageWriteOutput,
]):
    def read(
        self, cfg: Optional[DatasourceConfig]=None,
    ) -> ImageRead:
        return ImageRead(cfg)

    
    def write(
        self, cfg: Optional[DatasourceConfig]=None,
    ) -> ImageWrite:
        return ImageWrite(cfg)