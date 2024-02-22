from typing import Optional, Dict

from reportlab.lib.pagesizes import A4 # type: ignore

from core.datasource_level_2.schema import (
    DatasourceInput,
    DatasourceOutput
)

class PDFReadInput(DatasourceInput):
    path_to_file: str
    pages: Optional[list[int]] = None


class PDFReadOutput(DatasourceOutput):
    texts: Dict[int, str]


class PDFWriteInput(DatasourceInput):
    path_to_file: str
    text: str
    x_pending: float = 1
    y_pending: float = 1
    page_width: float = A4[0]
    page_height: float = A4[1]


class PDFWriteOutput(DatasourceOutput):
    ...