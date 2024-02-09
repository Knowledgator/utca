from typing import Dict, Any, Type, Optional

import PyPDF2
from reportlab.pdfgen.canvas import Canvas # type: ignore
from reportlab.lib.units import cm # type: ignore
from reportlab.lib.pagesizes import A4 # type: ignore

from core.datasource_level_2.datasource import DatasourceManager, DatasourceAction
from core.datasource_level_2.schema import (
    DatasourceConfig,
    DatasourceInput,
    DatasourceOutput
)

class PDFReadConfig(DatasourceConfig):
    ...


class PDFReadInput(DatasourceInput):
    path_to_file: str
    pages: Optional[list[int]] = None


class PDFReadOutput(DatasourceOutput):
    texts: Dict[int, str]


class PDFRead(DatasourceAction[
    PDFReadConfig,
    PDFReadInput,
    PDFReadOutput
]):
    input_class: Type[PDFReadInput] = PDFReadInput 
    output_class: Type[PDFReadOutput] = PDFReadOutput

    def __init__(self, cfg: Optional[PDFReadConfig]=None) -> None:
        super().__init__(cfg or PDFReadConfig())


    def invoke(self, input_data: PDFReadInput) -> Dict[str, Any]:
        with open(input_data.path_to_file, 'rb') as f:
            pdfReader = PyPDF2.PdfReader(f)
            pages = pdfReader.pages
            texts = {
                idx: pages[idx].extract_text()
                for idx in (input_data.pages or range(len(pages)))
            }
        return {'texts': texts}


    def invoke_batch(self, input_data: list[PDFReadInput]) -> list[Dict[str, Any]]:
        return [self.invoke(i) for i in input_data]


class PDFWriteConfig(DatasourceConfig):
    ...


class PDFWriteInput(DatasourceInput):
    path_to_file: str
    text: str
    x_pending: float = 1
    y_pending: float = 1
    page_width: float = A4[0]
    page_height: float = A4[1]


class PDFWriteOutput(DatasourceOutput):
    ...


class PDFWrite(DatasourceAction[
    PDFWriteConfig,
    PDFWriteInput,
    PDFWriteOutput
]):
    input_class: Type[PDFWriteInput] = PDFWriteInput 
    output_class: Type[PDFWriteOutput] = PDFWriteOutput
    
    def __init__(self, cfg: Optional[PDFWriteConfig]=None) -> None:
        super().__init__(cfg or PDFWriteConfig())


    def invoke(self, input_data: PDFWriteInput) -> Dict[str, Any]:
        canvas = Canvas(
            input_data.path_to_file, 
            pagesize=(input_data.page_width, input_data.page_height)
        )
        canvas.drawString( # type: ignore
            input_data.x_pending*cm, 
            input_data.page_height - input_data.y_pending*cm, 
            input_data.text
        ) 
        canvas.save()
        return {}


    def invoke_batch(self, input_data: list[PDFWriteInput]) -> list[Dict[str, Any]]:
        for i in input_data:
            self.invoke(i)
        return []


class PDFFile(DatasourceManager[
    PDFReadConfig,
    PDFReadInput,
    PDFReadOutput,

    PDFWriteConfig,
    PDFWriteInput,
    PDFWriteOutput,
]):
    def read(
        self, cfg: Optional[PDFReadConfig]=None,
    ) -> PDFRead:
        return PDFRead(cfg)

    
    def write(
        self, cfg: Optional[PDFWriteConfig]=None,
    ) -> PDFWrite:
        return PDFWrite(cfg)