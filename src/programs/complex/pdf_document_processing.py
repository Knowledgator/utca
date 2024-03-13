from typing import Any, Dict, List

from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.eval import (
    ForEach
)
from core.executable_level_1.memory import (
    SetMemory, GetMemory
)
from core.executable_level_1.actions import (
    AddData,
    UnpackValue,
    ExecuteFunction,
)
from implementation.datasources.pdf.actions import (
    PDFRead, PDFExtractTexts, PDFExtractImages, PDFFindTables
)
from implementation.tasks.text_processing.summarization.transformers.transformers_summarization import (
    SummarizationTask
)
from implementation.tasks.image_processing.documents_q_and_a.transformers.transformers_layout_lm import (
    DocumentQandATask
)

def prepare_text_summarization_input(
    input_data: Dict[str, Any]
) -> List[Dict[str, Any]]:
    return [
        {
            "inputs": text,
        } for text in input_data["pdf"]["texts"].values()
    ]


def prepare_image_classification_input(
    input_data: Dict[str, Any]
) -> List[Dict[str, Any]]:
    return [
        {
            "image": image.convert('RGB'),
            "page": page
        }
        for page, images in input_data["pdf"]["images"].items()
        for image in images
    ]


def crop_tables_from_pages(
    input_data: Dict[str, Any]
) -> List[Dict[str, Any]]:
    return [
        {
            "image": (
                input_data["pdf"]["pages"][page]
                .crop(table.bbox)
                .to_image(resolution=256)
                .original
            ),
            "page": page
        }
        for page, tables in input_data["pdf"]["tables"].items()
        for table in tables
    ]

if __name__ == "__main__":
    text_summarization = (
        PDFExtractTexts()
        | ExecuteFunction(prepare_text_summarization_input)
        | SummarizationTask()
    )

    process_visual_data = (
        SetMemory("image")
        | AddData({"question": "What is described here?"})
        | DocumentQandATask()
        | GetMemory(["image"])
        | UnpackValue("image")
    )

    image_processing = (
        PDFExtractImages()
        | ExecuteFunction(prepare_image_classification_input)
        | ForEach(
            process_visual_data
        )
    )

    table_processing = (
        PDFFindTables()
        | ExecuteFunction(crop_tables_from_pages)
        | ForEach(
            process_visual_data
        )
    )

    pipeline = (
        PDFRead()
        | SetMemory("pdf")
        | image_processing
        | SetMemory("images_descriptions")
        | GetMemory(["pdf"])
        | UnpackValue("pdf")
        # | table_processing
        # | SetMemory("tables_descriptions")
        # | GetMemory(["pdf"])
        # | UnpackValue("pdf")
        # | text_summarization
    )
    inputs = Evaluator(pipeline).run_program({
        "path_to_file": "programs/complex/pfizer-report.pdf",
        "pages": [10, 11, 12]
    })
    print(inputs)

