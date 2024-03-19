from typing import Any, Dict, List
import logging
import pathlib
PATH = pathlib.Path(__file__).parent.resolve()

from core.executable_level_1.interpreter import (
    Evaluator, EvaluatorConfigs
)
from core.executable_level_1.eval import (
    ForEach
)
from core.executable_level_1.memory import (
    SetMemory, 
    MemorySetInstruction,
    GetMemory, 
    MemoryGetInstruction,
)
from core.executable_level_1.actions import (
    Log,
    Flush,
    AddData,
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
            "page": page
        } for page, text in input_data["texts"].items()
    ]


def prepare_image_classification_input(
    input_data: Dict[str, Any]
) -> List[Dict[str, Any]]:
    return [
        {
            "image": image.convert('RGB'),
            "page": page
        }
        for page, images in input_data["images"].items()
        for image in images
    ]


def crop_tables_from_pages(
    input_data: Dict[str, Any]
) -> List[Dict[str, Any]]:
    return [
        {
            "image": (
                input_data["pdf"][page]
                .crop(table.bbox)
                .to_image(resolution=256)
                .original
            ),
            "page": page
        }
        for page, tables in input_data["tables"].items()
        for table in tables
    ]


def format_results_and_clean_up(input_data: Dict[str, Any]) -> Dict[str, Any]:
    info: Dict[str, Any] = {
        i: {
            "context": "",
            "tables": [],
            "images": []
        } for i in input_data["pages"] 
    }
    for s in input_data["summaries"]:
        info[s["page"]]["context"] = s["summary_text"]

    for t in input_data["tables_description"]:
        info[t["page"]]["tables"].append(
            t["answer"] or "Undefined table"
        )
        t["image"].close()

    for i in input_data["images_description"]:
        info[i["page"]]["images"].append(
            i["answer"] or "Undefined image"
        )
        i["image"].close()
    return info


if __name__ == "__main__":
    logger = logging.Logger("PipelineLogger")
    logger.addHandler(logging.StreamHandler())

    process_visual_data = (
        AddData({"question": "What is described here?"})
        | DocumentQandATask()
    )

    image_processing = (
        PDFExtractImages(resolution=256).use(
            get_key="pdf",
            set_key="images"
        )
        | ExecuteFunction(prepare_image_classification_input).use(
            set_key="images"
        )
        | Log(logger, "Images:")
        | ForEach(
            process_visual_data, 
            get_key="images",
            set_key="images_description"
        )
        | Flush(["images"])
        | Log(logger, "Images descriptions:")
        | SetMemory(
            set_key="images_description", 
            get_key="images_description",
            memory_instruction=MemorySetInstruction.MOVE
        )
    )

    table_processing = (
        PDFFindTables().use(
            get_key="pdf",
            set_key="tables"
        )
        | ExecuteFunction(crop_tables_from_pages).use(
            set_key="tables"
        )
        | Log(logger, "Tables:")
        | ForEach(
            process_visual_data, 
            get_key="tables",
            set_key="tables_description"
        )
        | Flush(["tables"])
        | Log(logger, "Tables descriptions:")
        | SetMemory(
            set_key="tables_description", 
            get_key="tables_description",
            memory_instruction=MemorySetInstruction.MOVE
        ) 
    )

    text_summarization = (
        PDFExtractTexts(tables=False).use(
            get_key="pdf",
            set_key="texts"
        )
        | ExecuteFunction(
            prepare_text_summarization_input
        ).use(set_key="texts")
        | Log(logger, "Texts:")
        | SummarizationTask().use(
            get_key="texts",
            set_key="summaries"
        )
        | Flush(["texts"])
        | Log(logger, "Summaries:")
        | SetMemory(
            set_key="summaries", 
            get_key="summaries",
            memory_instruction=MemorySetInstruction.MOVE
        ) 
    )

    pipeline = (
        SetMemory(set_key="pages", get_key="pages")
        | PDFRead().use(
            set_key="pdf"
        )
        | Log(logger, "Read:")
        | image_processing
        | table_processing
        | text_summarization
        | Flush()
        | GetMemory(
            ["pages", "tables_description", "images_description", "summaries"], 
            memory_instruction=MemoryGetInstruction.POP
        )
        | ExecuteFunction(format_results_and_clean_up)
        | Log(logger, "Result:", open="="*40, close="="*40)
    )
    inputs = Evaluator(
        pipeline,
        cfg=EvaluatorConfigs()
    ).run_program({
        "path_to_file": f"{PATH}/pfizer-report.pdf",
        "pages": [10, 11, 12]
    })
