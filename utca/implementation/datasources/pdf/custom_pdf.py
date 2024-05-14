# 1. extract tables boxes. 
# 2. exclude/include and format text
from typing import List, Any, Dict, Tuple, Optional
from operator import itemgetter

from pdfminer.pdfpage import PDFPage
from pdfplumber.page import Page
from pdfplumber.pdf import PDF
from pdfplumber._typing import T_num,  T_bbox, T_obj, T_obj_list
from pdfplumber.table import Table
from pdfplumber.utils.text import TextMap, extract_text, chars_to_textmap


def char_in_bbox(char: T_obj, bbox: T_bbox) -> bool:
    v_mid = (char["top"] + char["bottom"]) / 2
    h_mid = (char["x0"] + char["x1"]) / 2
    x0, top, x1, bottom = bbox
    return (
        (h_mid >= x0) 
        and (h_mid < x1) 
        and (v_mid >= top) 
        and (v_mid < bottom)
    )


def extract_chars(
    bbox: T_bbox, chars: T_obj_list
) -> Tuple[T_obj_list, T_obj_list]:
    extracted_chars: T_obj_list = []
    unprocessed_chars: T_obj_list = []
    for char in chars:
        if char_in_bbox(char, bbox):
            extracted_chars.append(char)
        else:
            unprocessed_chars.append(char)
    return unprocessed_chars, extracted_chars


def process_tables_chars(
    tables: List[Table], 
    unprocessed_chars: T_obj_list, 
    **kwargs: Any
) -> Tuple[List[List[List[Optional[str]]]], T_obj_list]:
    extracted_tables: List[List[List[Optional[str]]]] = []
    for table in tables:
        table_arr: List[List[Optional[str]]] = []
        for row in table.rows:
            arr: List[Optional[str]] = []
            unprocessed_chars, row_chars = extract_chars(row.bbox, unprocessed_chars)

            for cell in row.cells:
                if cell is None:
                    cell_text = None
                else:
                    row_chars, cell_chars = extract_chars(cell, row_chars)

                    if len(cell_chars):
                        kwargs["x_shift"] = cell[0]
                        kwargs["y_shift"] = cell[1]
                        if "layout" in kwargs:
                            kwargs["layout_width"] = cell[2] - cell[0]
                            kwargs["layout_height"] = cell[3] - cell[1]
                        cell_text = extract_text(cell_chars, **kwargs)
                    else:
                        cell_text = ""
                arr.append(cell_text)
            table_arr.append(arr)
        extracted_tables.append(table_arr)
    return extracted_tables, unprocessed_chars


def get_markdown_table(table: List[List[Optional[str]]]) -> str:
    table_md = ""
    for row in table:
        table_md += "| "
        for cell in row:
            if cell:
                table_md += cell.replace("\n", "<br/>") + " |"
            else:
                table_md += "|"
        table_md += "\n"
    return table_md


class CustomPage(Page):
    def __init__(
        self,
        pdf: "PDF",
        page_obj: PDFPage,
        page_number: int,
        initial_doctop: T_num = 0,
    ):
        super().__init__(
            pdf,
            page_obj,
            page_number,
            initial_doctop,
        )
        self.get_textmap = self._custom_get_textmap


    def _custom_get_textmap(self, chars: T_obj_list, **kwargs: Any) -> TextMap:
        defaults = dict(x_shift=self.bbox[0], y_shift=self.bbox[1])
        if "layout_width_chars" not in kwargs:
            defaults.update({"layout_width": self.width})
        if "layout_height_chars" not in kwargs:
            defaults.update({"layout_height": self.height})
        full_kwargs: Dict[str, Any] = {**defaults, **kwargs}
        return chars_to_textmap(
            chars, **full_kwargs
        )


    def extract_text(self, **kwargs: Any) -> str:
        tables = self.find_tables(kwargs.get("table_settings", {}))

        if tables:
            processed_tables, unprocessed_chars = process_tables_chars(
                tables, self.chars
            )
        else:
            processed_tables, unprocessed_chars = [], self.chars

        text_map = self.get_textmap(unprocessed_chars, **kwargs)
        
        if not kwargs.get("tables") or not tables:
            return text_map.as_string
        
        current_table = 0
        text = ""
        for idx, t in enumerate(text_map.tuples):
            if current_table >= len(tables):
                text += "".join(map(itemgetter(0), text_map.tuples[idx:]))
                break

            char, meta = t[0], t[1]
            if not meta or meta["top"] < tables[current_table].bbox[1] :
                text += char
            else:
                if meta["x0"] >= tables[current_table].bbox[0]:
                    text += get_markdown_table(processed_tables[current_table])
                    current_table += 1
                text += char
        return text


class CustomPDF(PDF):
    @property
    def pages(self) -> List[Page]:
        if hasattr(self, "_pages"):
            return self._pages

        doctop: T_num = 0
        pp = self.pages_to_parse
        self._pages: List[Page] = []
        for i, page in enumerate(PDFPage.create_pages(self.doc)):
            page_number = i + 1
            if pp is not None and page_number not in pp:
                continue
            p = CustomPage(
                self, 
                page, 
                page_number=page_number, 
                initial_doctop=doctop
            )
            self._pages.append(p)
            doctop += p.height
        return self._pages