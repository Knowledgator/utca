from typing import Dict, Any

from core.executable_level_1.eval import Evaluator
from core.executable_level_1.schema import (
    ExecuteFunction,
)
from implementation.datasources.google_docs.google_docs import (
    GoogleDocsClientConfig,
    GoogleDocsClient,
    GoogleDocsReadInput,
)
from implementation.models.token_searcher.model import (
    TokenSearcherModel, TokenSearcherModelConfig
)

def get_text(input: Dict[str, Any]) -> Dict[str, Any]:
    text = ''.join((
        t.get('textRun', {}).get('content', '')
        for i in input['body']['content']
        if 'paragraph' in i
        for t in i['paragraph']['elements']
    ))
    return {'text': text}


def set_prompt(input: Dict[str, Any]) -> Dict[str, Any]:
    prompt = 'Identify organizations mentioned in the text: {}'
    return {
        'inputs': [prompt.format(input['text'])]
    }


if __name__ == '__main__':
    # Google Docs client
    docs = GoogleDocsClient(
        GoogleDocsClientConfig(
            credentials='credentials.json',
            # path to your credentials. 
            # Can be not provided if you are using 
            # environment credentials for Google cloud.
            scopes = [
                "https://www.googleapis.com/auth/documents"
                # read and write scope
            ]
        )
    )

    # model that will be used
    model = TokenSearcherModel(
        TokenSearcherModelConfig(
            device = 'cpu'
        )
    )

    document_id = '1qDrWeHqblOOakVCIc7FJUr8u2rAhRdj2YSb4SgTz96g'# 'your_document_id'
    # can be found in url: https://docs.google.com/document/d/***document_id***/edit
    
    # create pipeline with described stages
    pipeline = (
        docs.read()
        | ExecuteFunction(get_text)
        | ExecuteFunction(set_prompt)
        | model
    )

    read_input = GoogleDocsReadInput(
        document_id=document_id
    )
    print(Evaluator(pipeline).run(read_input))
    # result should be written to specified spreadsheet