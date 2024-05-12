from typing import Dict, Any
import pathlib
PATH = pathlib.Path(__file__).parent.resolve()

from core import (
    ExecuteFunction,
    AddData,
    RenameAttribute
)
from implementation.datasources.pdf import (
    PDFRead, PDFExtractTexts
)
from implementation.predictors import (
    TokenSearcherPredictor, TokenSearcherPredictorConfig
)
from implementation.tasks import (
    TokenSearcherTextCleaner,
    TokenSearcherTextCleanerPostprocessor,
    TokenSearcherNER,
    TokenSearcherNERPostprocessor,
)

def get_page_text(input: Dict[int, Any]) -> Dict[str, Any]:
    return {"text": input[1]}


if __name__ == "__main__":
    # model that will be used for clean text and NER tasks
    model = TokenSearcherPredictor(
        TokenSearcherPredictorConfig(
            device="cpu"
        )
    )

    # clean text stage
    clean_task = TokenSearcherTextCleaner(
        predictor=model,
        postprocess=[TokenSearcherTextCleanerPostprocessor(
            clean=True,
        )]
    )

    # NER stage
    ner_task = TokenSearcherNER(
        predictor=model,
        postprocess=[TokenSearcherNERPostprocessor(
            threshold=0.8
        )]
    )

    # create pipeline with described stages
    pipeline = (
        PDFRead().use(set_key="pdf")
        | PDFExtractTexts().use(
            get_key="pdf", 
            set_key="texts"
        )
        | ExecuteFunction(get_page_text).use(get_key="texts")
        # adapts outputs to inputs 
        
        | clean_task
        | RenameAttribute("cleaned_text", "text")         
        | AddData({"labels": ["person", "framework"]}) 
        # add labels that will be used by NER task
        
        | ner_task
    )

    # call pipeline
    res = pipeline.run({
        "path_to_file": f"{PATH}/test.pdf"
    })

    print(res)