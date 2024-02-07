from typing import Dict, Any
import logging

from core.executable_level_1.eval import Evaluator
from core.executable_level_1.schema import (
    ExecuteFunction,
    AddData
)
from core.datasource_level_2.pdf import (
    PDFReadConfig, PDFReadInput,
    PDFFile
)
from implementation.models.token_searcher.model import (
    TokenSearcherModel, TokenSearcherModelConfig
)
from implementation.tasks.clean_text.token_searcher import (
    TokenSearcherTextCleanerTask, TokenSearcherTextCleanerConfig
)
from implementation.models.token_searcher.model import (
    TokenSearcherModel, TokenSearcherModelConfig
)
from implementation.tasks.ner.token_searcher import (
    TokenSearcherNERConfig, TokenSearcherNERTask
)

def test_pipeline():
    file = PDFFile()
    read_input = PDFReadInput(
        path_to_file='src/core/__test__/test.pdf'
    )
    read_pdf = file.read(PDFReadConfig())

    model = TokenSearcherModel(TokenSearcherModelConfig(
        name="knowledgator/UTC-DeBERTa-small"
    ))

    clean_task = TokenSearcherTextCleanerTask(
        TokenSearcherTextCleanerConfig(clean=True),
        model
    )

    ner_task = TokenSearcherNERTask(
        TokenSearcherNERConfig(
            threshold=0.8
        ),
        model
    )

    def get_page(input: Dict[str, Any]) -> Dict[str, Any]:
        return {'text': input['texts'][0]}


    def get_ner_input(input: Dict[str, Any]) -> Dict[str, Any]:
        return {'text': input['cleaned_text']}


    pipeline = (
        read_pdf 
        | ExecuteFunction(get_page) 
        | clean_task 
        | ExecuteFunction(get_ner_input)
        | AddData({'labels': ['people', 'framework']}) 
        | ner_task
    )
    res = Evaluator(pipeline).run(read_input)

    logging.error(res)