from typing import Optional

from core.datasource_level_2.datasource import DatasourceManager
from core.datasource_level_2.schema import DatasourceConfig
from implementation.datasources.pdf.schema import (
    PDFReadInput,
    PDFReadOutput,
    PDFWriteInput,
    PDFWriteOutput
)
from implementation.datasources.pdf.actions import (
    PDFRead,
    PDFWrite
)

class PDFFile(DatasourceManager[
    DatasourceConfig,
    PDFReadInput,
    PDFReadOutput,

    DatasourceConfig,
    PDFWriteInput,
    PDFWriteOutput,
]):
    def read(
        self, cfg: Optional[DatasourceConfig]=None,
    ) -> PDFRead:
        return PDFRead(cfg)

    
    def write(
        self, cfg: Optional[DatasourceConfig]=None,
    ) -> PDFWrite:
        return PDFWrite(cfg)