from typing import Dict, Any

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
from implementation.tasks.ner.token_searcher import (
    TokenSearcherNERConfig, TokenSearcherNERTask
)

def get_page(input: Dict[str, Any]) -> Dict[str, Any]:
    return {'text': input['texts'][0]}


def get_ner_input(input: Dict[str, Any]) -> Dict[str, Any]:
    return {'text': input['cleaned_text']}


if __name__ == '__main__':
    # stage for PDF reading
    read_pdf = PDFFile().read(PDFReadConfig())

    # model that will be used for clean text and NER tasks
    model = TokenSearcherModel(TokenSearcherModelConfig(
        name="knowledgator/UTC-DeBERTa-small"
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
    pipeline = (
        read_pdf 
        | ExecuteFunction(get_page) 
        # adapts outputs to inputs 
        
        | clean_task 
        | ExecuteFunction(get_ner_input)         
        | AddData({'labels': ['person', 'framework']}) 
        # add labels that will be used by NER task
        
        | ner_task
    )

    # parameters for pdf file reading
    read_input = PDFReadInput(
        path_to_file='programs/program1/test.pdf'
    )

    # call pipeline
    res = Evaluator(pipeline).run(read_input)

    print(res)