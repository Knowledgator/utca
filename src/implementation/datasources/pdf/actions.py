from typing import Dict, Any, List, Iterator
import io

from PIL import Image
from reportlab.pdfgen.canvas import Canvas # type: ignore
from reportlab.lib.units import cm # type: ignore
from reportlab.lib.pagesizes import A4 # type: ignore

from core.executable_level_1.actions import Action
from implementation.datasources.pdf.custom_pdf import CustomPDF, Page, Table

class PDFRead(Action[Dict[str, Any], Dict[int, Page]]):
    def execute(self, input_data: Dict[str, Any]) -> Dict[int, Page]:
        pdfReader = CustomPDF.open(
            input_data['path_to_file'], 
            pages=input_data.get('pages')
        )
        return {
            page.page_number: page
            for page in pdfReader.pages
        }


class PDFExtractTexts(Action[Dict[int, Page], Dict[int, str]]):
    def __init__(self, tables: bool=True) -> None:
        self.tables = tables
    

    def execute(self, input_data: Dict[int, Page]) -> Dict[int, str]:
        return {
            page_id: page.extract_text(tables=self.tables)
            for page_id, page in input_data.items()
        }


class PDFFindTables(Action[Dict[int, Page], Dict[int, List[Table]]]):
    def execute(self, input_data: Dict[int, Page]) -> Dict[int, List[Table]]:
        return {
            page_id: page.find_tables()
            for page_id, page in input_data.items()
        }


class PDFExtractTables(Action[Dict[int, Page], Dict[int, Any]]):
    def execute(self, input_data: Dict[int, Page]) -> Dict[int, Any]:
        return {
            page_id: page.extract_tables()
            for page_id, page in input_data.items()
        }
            

class PDFExtractImages(Action[Dict[int, Page], Dict[int, Any]]):
    resolution: int 
    def __init__(self, resolution: int=72) -> None:
        self.resolution = resolution
    
    def extract_images_from_page(self, page: Page, resolution: int) -> Iterator[Image.Image]:
        page_height = page.height

        for image in page.images:
            image_bbox = (image['x0'], page_height - image['y1'], image['x1'], page_height - image['y0'])
            cropped_page = page.crop(image_bbox)
            tmp = io.BytesIO()
            cropped_page.to_image(resolution=resolution).save(tmp)
            yield Image.open(tmp)


    def execute(self, input_data: Dict[int, Page]) -> Dict[int, Any]:
        return {
            page_id: list(self.extract_images_from_page(
                page, 
                resolution=self.resolution
            )) for page_id, page in input_data.items()
        }


class PDFWrite(Action[Dict[str, Any], None]):
    def execute(self, input_data: Dict[str, Any]) -> None:
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