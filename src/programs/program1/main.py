from typing import Dict, Any

from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.eval import ExecutionSchema
from core.executable_level_1.actions import (
    ExecuteFunction,
    AddData
)
from implementation.datasources.pdf.actions import (
    PDFRead
)
from implementation.predictors.token_searcher.predictor import (
    TokenSearcherPredictor, TokenSearcherPredictorConfig
)
from implementation.tasks.clean_text.token_searcher import (
    TokenSearcherTextCleanerTask, TokenSearcherTextCleanerConfig
)
from implementation.tasks.ner.token_searcher import (
    TokenSearcherNERConfig, TokenSearcherNERTask
)

def get_page(input: Dict[str, Any]) -> Dict[str, Any]:
    return {"text": input["texts"][0]}


def get_ner_input(input: Dict[str, Any]) -> Dict[str, Any]:
    return {"text": input["cleaned_text"]}


if __name__ == "__main__":
    # model that will be used for clean text and NER tasks
    model = TokenSearcherPredictor(TokenSearcherPredictorConfig(
        device = "cpu"
    ))

    # clean text stage
    clean_task = TokenSearcherTextCleanerTask(
        TokenSearcherTextCleanerConfig(clean=True),
        model
    )

    # NER stage
    ner_task = TokenSearcherNERTask(
        TokenSearcherNERConfig(
            threshold=0.8
        ),
        model
    )

    # create pipeline with described stages
    pipeline: ExecutionSchema = (
        PDFRead()
        | ExecuteFunction(get_page) 
        # adapts outputs to inputs 
        
        | clean_task 
        | ExecuteFunction(get_ner_input)         
        | AddData({"labels": ["person", "framework"]}) 
        # add labels that will be used by NER task
        
        | ner_task
    )

    # call pipeline
    res = Evaluator(pipeline).run_program({
        "path_to_file": "programs/program1/test.pdf"
    })

    print(res)