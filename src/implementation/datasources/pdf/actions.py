from typing import Dict, Any, Iterator, cast
import io

from PIL import Image
from reportlab.pdfgen.canvas import Canvas # type: ignore
from reportlab.lib.units import cm # type: ignore
from reportlab.lib.pagesizes import A4 # type: ignore

from core.executable_level_1.actions import OneToOne
from implementation.datasources.pdf.custom_pdf import CustomPDF, Page

class PDFRead(OneToOne):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pdfReader = CustomPDF.open(
            input_data['path_to_file'], 
            pages=input_data.get('pages')
        )
        input_data["pdf"] = {
            "pages": {
                page.page_number: page
                for page in pdfReader.pages
            }
        }
        return input_data


class PDFExtractTexts(OneToOne):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data["pdf"]["texts"] = {
            page_id: cast(Page, page).extract_text(tables=input_data.get("tables"))
            for page_id, page in input_data["pdf"]["pages"].items()
        }
        return input_data


class PDFFindTables(OneToOne):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data["pdf"]["tables"] = {
            page_id: cast(Page, page).find_tables()
            for page_id, page in input_data["pdf"]["pages"].items()
        }
        return input_data


class PDFExtractTables(OneToOne):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data["pdf"]["extracted_tables"] = {
            page_id: cast(Page, page).extract_tables()
            for page_id, page in input_data["pdf"]["pages"].items()
        }
        return input_data
            

class PDFExtractImages(OneToOne):
    def extract_images_from_page(self, page: Page) -> Iterator[Image.Image]:
        page_height = page.height

        for image in page.images:
            image_bbox = (image['x0'], page_height - image['y1'], image['x1'], page_height - image['y0'])
            cropped_page = page.crop(image_bbox)
            tmp = io.BytesIO()
            cropped_page.to_image(resolution=1024).save(tmp)
            yield Image.open(tmp)


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        images: Dict[str, Any] = {}
        for page_id, page in input_data["pdf"]["pages"].items():
            images[page_id] = list(self.extract_images_from_page(cast(Page, page)))
        input_data["pdf"]["images"] = images
        return input_data


class PDFWrite(OneToOne):
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