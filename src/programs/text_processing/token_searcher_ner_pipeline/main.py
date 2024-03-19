from typing import Dict, Any
import pathlib
PATH = pathlib.Path(__file__).parent.resolve()

from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.eval import ExecutionSchema
from core.executable_level_1.actions import (
    ExecuteFunction,
    AddData,
    RenameAttribute
)
from implementation.datasources.pdf.actions import (
    PDFRead, PDFExtractTexts
)
from implementation.predictors.token_searcher.predictor import (
    TokenSearcherPredictor, TokenSearcherPredictorConfig
)
from implementation.tasks.text_processing.clean_text.token_searcher.token_searcher import (
    TokenSearcherTextCleanerTask
)
from implementation.tasks.text_processing.clean_text.token_searcher.actions import (
    TokenSearcherTextCleanerPostprocessor,
    TokenSearcherTextCleanerPostprocessorConfig
)
from implementation.tasks.text_processing.ner.token_searcher.token_searcher import (
    TokenSearcherNERTask
)
from implementation.tasks.text_processing.ner.token_searcher.actions import (
    TokenSearcherNERPostprocessor,
    TokenSearcherNERPostprocessorConfig

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
    clean_task = TokenSearcherTextCleanerTask(
        predictor=model,
        postprocess=[TokenSearcherTextCleanerPostprocessor(
            TokenSearcherTextCleanerPostprocessorConfig(clean=True),
        )]
    )

    # NER stage
    ner_task = TokenSearcherNERTask(
        predictor=model,
        postprocess=[TokenSearcherNERPostprocessor(
            TokenSearcherNERPostprocessorConfig(
                threshold=0.8
            )
        )]
    )

    # create pipeline with described stages
    pipeline: ExecutionSchema = (
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
    res = Evaluator(pipeline).run_program({
        "path_to_file": f"{PATH}/test.pdf"
    })

    print(res)