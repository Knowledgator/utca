from typing import Type, Dict, Any

import PyPDF2
from reportlab.pdfgen.canvas import Canvas # type: ignore
from reportlab.lib.units import cm # type: ignore

from core.datasource_level_2.schema import DatasourceConfig
from core.datasource_level_2.datasource import DatasourceAction
from implementation.datasources.pdf.schema import (
    PDFReadInput,
    PDFReadOutput,
    PDFWriteInput,
    PDFWriteOutput
)

class PDFRead(DatasourceAction[
    DatasourceConfig,
    PDFReadInput,
    PDFReadOutput
]):
    input_class: Type[PDFReadInput] = PDFReadInput 
    output_class: Type[PDFReadOutput] = PDFReadOutput

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


class PDFWrite(DatasourceAction[
    DatasourceConfig,
    PDFWriteInput,
    PDFWriteOutput
]):
    input_class: Type[PDFWriteInput] = PDFWriteInput 
    output_class: Type[PDFWriteOutput] = PDFWriteOutput

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