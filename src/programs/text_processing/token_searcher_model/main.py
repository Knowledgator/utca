from typing import Dict, Any

from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.actions import (
    ExecuteFunction
)
from implementation.apis.google_cloud.client import GoogleCloudClient
from implementation.datasources.google_docs.schema import (
    GoogleDocsClientConfig
)
from implementation.datasources.google_docs.actions import (
    GoogleDocsRead
)
from implementation.predictors.token_searcher.predictor import (
    TokenSearcherPredictor, TokenSearcherPredictorConfig
)

def get_text(input: Dict[str, Any]) -> Dict[str, Any]:
    text = "".join((
        t.get("textRun", {}).get("content", "")
        for i in input["body"]["content"]
        if "paragraph" in i
        for t in i["paragraph"]["elements"]
    ))
    return {"text": text}


def set_prompt(input: Dict[str, Any]) -> Dict[str, Any]:
    prompt = "Identify organizations mentioned in the text: {}"
    return {
        "inputs": [prompt.format(input["text"])]
    }


if __name__ == "__main__":
    # Google Docs client
    client = GoogleCloudClient(
        GoogleDocsClientConfig(
            credentials="credentials.json",
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
    model = TokenSearcherPredictor(
        TokenSearcherPredictorConfig(
            device = "cpu"
        )
    )

    document_id = "1qDrWeHqblOOakVCIc7FJUr8u2rAhRdj2YSb4SgTz96g"#"your_document_id"
    # can be found in url: https://docs.google.com/document/d/***document_id***/edit
    
    # create pipeline with described stages
    pipeline = (
        GoogleDocsRead(client)
        | ExecuteFunction(get_text)
        | ExecuteFunction(set_prompt)
        | model
    )

    print(Evaluator(pipeline).run_program({
        "document_id": document_id
    }))
    # result should be written to specified spreadsheet