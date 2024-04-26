from typing import Dict, Any, List, Iterator, Optional

from PIL import Image
from reportlab.pdfgen.canvas import Canvas # type: ignore
from reportlab.lib.units import cm # type: ignore
from reportlab.lib.pagesizes import A4 # type: ignore

from core.executable_level_1.actions import Action
from implementation.datasources.pdf.custom_pdf import CustomPDF, Page, Table

class PDFRead(Action[Dict[str, Any], Dict[int, Page]]):
    """
    Read PDF document
    """
    def execute(self, input_data: Dict[str, Any]) -> Dict[int, Page]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'path_to_file' (str): Path to PDF file;

                'pages' (List[int], optional): Pages to read. If not provided,
                    read complete document;

        Returns:
            Dict[int, Page]: PDF;
        """
        pdfReader = CustomPDF.open(
            input_data["path_to_file"], 
            pages=input_data.get("pages")
        )
        return {
            page.page_number: page
            for page in pdfReader.pages
        }


class PDFExtractTexts(Action[Dict[int, Page], Dict[int, str]]):
    """
    Extract texts from pages
    """
    def __init__(self, tables: bool=True, name: Optional[str]=None) -> None:
        """
        Args:
            tables (bool, optional): If equals to True, include text from tables.
                Defaults to True.
            
            name (Optional[str], optional): name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.tables = tables
    

    def execute(self, input_data: Dict[int, Page]) -> Dict[int, str]:
        """
        Args:
            input_data (Dict[int, Page]): PDF document;

        Returns:
            Dict[int, str]: Extracted texts;
        """
        return {
            page_id: page.extract_text(tables=self.tables)
            for page_id, page in input_data.items()
        }


class PDFFindTables(Action[Dict[int, Page], Dict[int, List[Table]]]):
    """
    Find tables on pages
    """
    def execute(self, input_data: Dict[int, Page]) -> Dict[int, List[Table]]:
        """
        Args:
            input_data (Dict[int, Page]): PDF document;

        Returns:
            Dict[int, Table]: Founded tables;
        """
        return {
            page_id: page.find_tables()
            for page_id, page in input_data.items()
        }


class PDFExtractTables(Action[Dict[int, Page], Dict[int, Any]]):
    """
    Extract tables from pages
    """
    def execute(self, input_data: Dict[int, Page]) -> Dict[int, Any]:
        """
        Args:
            input_data (Dict[int, Page]): PDF document;

        Returns:
           Dict[int, Any]: Extracted tables;
        """
        return {
            page_id: page.extract_tables()
            for page_id, page in input_data.items()
        }
            

class PDFExtractImages(Action[Dict[int, Page], Dict[int, Any]]):
    """
    Extract images from pages
    """
    resolution: int 
    def __init__(self, resolution: int=72, name: Optional[str]=None) -> None:
        """
        Args:
            resolution (int, optional): Images resolution. Defaults to 72.
            
            name (Optional[str], optional): name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.resolution = resolution


    def extract_images_from_page(self, page: Page, resolution: int) -> Iterator[Image.Image]:
        page_height = page.height

        for image in page.images:
            image_bbox = (
                image["x0"], 
                page_height - image["y1"], 
                image["x1"], 
                page_height - image["y0"]
            )
            yield (
                page
                .crop(image_bbox)
                .to_image(resolution=resolution)
                .original
            )


    def execute(self, input_data: Dict[int, Page]) -> Dict[int, Any]:
        """
        Args:
            input_data (Dict[int, Page]): PDF document;

        Returns:
            Dict[int, Any]: Extracted images;
        """
        return {
            page_id: list(self.extract_images_from_page(
                page, 
                resolution=self.resolution
            )) for page_id, page in input_data.items()
        }


class PDFWrite(Action[Dict[str, Any], None]):
    """
    Write PDF file
    """
    def execute(self, input_data: Dict[str, Any]) -> None:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'path_to_file' (str): Path to PDF file;

                'page_width' (float, optional): Page width in cm;

                'page_height' (float, optional): Page height in cm;

                'x_padding' (float, optional): x padding in cm;

                'y_padding' (float, optional): y padding in cm;

                'text' (str): text to write;
        """
        canvas = Canvas(
            input_data["path_to_file"], 
            pagesize=(
                input_data.get("page_width", 0)*cm or A4[0], 
                input_data.get("page_height", 0)*cm or  A4[1]
            )
        )
        canvas.drawString( # type: ignore
            input_data.get("x_padding", 0)*cm, 
            input_data.get("y_padding", 0)*cm, 
            input_data["text"]
        ) 
        canvas.save()