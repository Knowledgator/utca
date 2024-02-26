from typing import Dict, Any, List, Optional, Iterator, cast
import re
import io

from PIL import Image
import pdfplumber
from pdfplumber.page import Page
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure, LTPage
from reportlab.pdfgen.canvas import Canvas # type: ignore
from reportlab.lib.units import cm # type: ignore
from reportlab.lib.pagesizes import A4 # type: ignore

from core.executable_level_1.actions import (
    OneToOne,
    Action
)

@OneToOne
class PDFRead(Action):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pdfReader = pdfplumber.open(
            input_data['path_to_file'], 
            pages=input_data.get('pages')
        )
        return {
            "pdf": {
                page.page_number: page
                for page in pdfReader.pages
            }
        }


class PDFExtractTexts(Action):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "pdf_texts": {
                page_id: cast(Page, page).extract_text()
                for page_id, page in input_data["pdf"].items()
            }
        }
    

@OneToOne
class PDFExtractTextsFormatted(Action):
    def process_page(
        self, 
        page: Page, 
        ex_tables: bool=True
    ) -> str:
        content: List[str] = []
        
        # Find the tables in the page
        tables = page.find_tables()
        extracted_tables = page.extract_tables()


        table_num = 0
        first_table_element = True
        table_extraction_process = False


        # Get a sorted list of elements based on their Y-coordinate in reverse order
        elements = [element for element in page.layout]
        elements.sort(key=lambda a: a.y1, reverse=True)


        lower_side = 0
        upper_side = 0
        for i, element in enumerate(elements):
            # Extract text if the element is a text container and text extraction is enabled
            if isinstance(element, LTTextContainer) and not table_extraction_process and ex_text:
                line_text = self.text_extraction(cast(LTTextContainer[Any], element))
                content.append(line_text)


            # Process tables if the element is a rectangle and table extraction is enabled
            if isinstance(element, LTRect) and ex_table:
                if first_table_element and table_num < len(tables):
                    lower_side = page.bbox[3] - tables[table_num].bbox[3]
                    upper_side = element.y1


                    table = extracted_tables[table_num]
                    table_string = self.convert_table(table)
                    content.append(table_string)
                    table_extraction_process = True
                    first_table_element = False


                # Check if we have already extracted the tables from the page
                if element.y0 >= lower_side and element.y1 <= upper_side:
                    pass
                elif i + 1 >= len(elements):
                    pass
                elif not isinstance(elements[i + 1], LTRect):
                    table_extraction_process = False
                    first_table_element = True
                    table_num += 1


        # Combine and clean up the extracted content
        return re.sub('\n+', '\n', ''.join(content))
    

    def normalize_text(self, line_texts: List[str]) -> str:
        norm_text = ''
        for line_text in line_texts:
            line_text=line_text.strip()
            # empty strings after striping convert to newline character
            if not line_text:
                line_text = '\n'
            else:
                line_text = re.sub(r'\s+', ' ', line_text)
                # if the last character is not a letter or number, add newline character to a line
                if not re.search(r'[\w\d\,\-]', line_text[-1]):
                    line_text+='\n'
                else:
                    line_text+=' '
            # concatenate into single string
            norm_text+=line_text
        return norm_text


    def text_extraction(self, element: LTTextContainer[Any]) -> str:
        # Extract text from line and split it with new lines
        line_texts = element.get_text().split('\n')
        line_text = self.normalize_text(line_texts)
        return line_text


    def convert_table(self, table: List[List[Optional[str]]]) -> str:
        table_string = ''
        # iterate through rows in the table
        for row in table:
            # clean row from newline character
            cleaned_row = [
                'None' if item is None else item.replace('\n', ' ')
                for item in row
            ]
            # concatenate the row as a string with the whole table
            table_string += f"|{'|'.join(cleaned_row)}|\n"
        return table_string.rstrip('\n')


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            page_id: self.process_page(page)
            for page_id, page in input_data["pdf"].items()
        }


@OneToOne
class PDFExtractTables(Action):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "pdf_tables": {
                page_id: cast(Page, page).extract_tables()
                for page_id, page in input_data["pdf"].items()
            }
        }
    

@OneToOne
class PDFExtractImages(Action):
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
        for page_id, page in input_data["pdf"].items():
            images[page_id] = list(self.extract_images_from_page(cast(Page, page)))
        return {
            "pdf_images": images
        }


@OneToOne
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