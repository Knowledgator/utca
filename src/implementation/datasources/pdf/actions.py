from typing import Dict, Any

import PyPDF2
from reportlab.pdfgen.canvas import Canvas # type: ignore
from reportlab.lib.units import cm # type: ignore
from reportlab.lib.pagesizes import A4 # type: ignore

from core.executable_level_1.actions import Action

class PDFRead(Action):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        with open(input_data['path_to_file'], 'rb') as f:
            pdfReader = PyPDF2.PdfReader(f)
            pages = pdfReader.pages
            texts: Dict[int, str] = {
                idx: pages[idx].extract_text() # type: ignore
                for idx in (input_data.get('pages', range(len(pages))))
            }
        input_data['texts'] = texts
        return input_data


class PDFWrite(Action):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        canvas = Canvas(
            input_data['path_to_file'], 
            pagesize=(
                input_data.get('page_width') or A4[0], 
                input_data.get('page_height') or  A4[1]
            )
        )
        canvas.drawString( # type: ignore
            input_data.get('x_pending', 0)*cm, 
            input_data.get('y_pending', 0)*cm, 
            input_data['text']
        ) 
        canvas.save()
        return input_data