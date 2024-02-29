from typing import Dict, Any

from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.eval import ExecutionSchema
from core.executable_level_1.actions import (
    OneToOne,
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

def get_page(input: Dict[str, Any]) -> Dict[str, Any]:
    return {"text": input["pdf_texts"][1]}


if __name__ == "__main__":
    # model that will be used for clean text and NER tasks
    model = TokenSearcherPredictor(TokenSearcherPredictorConfig(
        device = "cpu"
    ))

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
        PDFRead()
        | PDFExtractTexts()
        | OneToOne(ExecuteFunction)(get_page) 
        # adapts outputs to inputs 
        
        | clean_task 
        | RenameAttribute("cleaned_text", "text")         
        | AddData({"labels": ["person", "framework"]}) 
        # add labels that will be used by NER task
        
        | ner_task
    )

    # call pipeline
    res = Evaluator(pipeline).run_program({
        "path_to_file": "programs/text_processing/token_searcher_ner_pipeline/test.pdf"
    })

    print(res)