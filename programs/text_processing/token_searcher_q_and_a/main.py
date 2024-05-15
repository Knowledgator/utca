from typing import Dict, Any
import pathlib
PATH = pathlib.Path(__file__).parent.resolve()

from utca.core import (
    ExecuteFunction,
    AddData,
)
from utca.implementation.apis.google_cloud import GoogleCloudClient
from utca.implementation.datasources.google_sheets import (
    GoogleSheetsClientConfig,
    GoogleSheetsRead,
    GoogleSheetsWrite,
    Dimension,
)
from utca.implementation.predictors import (
    TokenSearcherPredictor, 
    TokenSearcherPredictorConfig
)
from utca.implementation.tasks import (
    TokenSearcherQandA,
    TokenSearcherQandAPostprocessor,
)

def get_input_for_q_and_a(input: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "text": input["table"][0][0],
        "question": input["table"][0][1]
    }


def create_table(input: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "table": [
            [f"Answer {i+1}", input["output"][i]["span"]]
            for i in range(len(input["output"]))
        ],
        "dimension": Dimension.COLUMNS
    }


if __name__ == "__main__":
    # Google Spreadsheet client
    client = GoogleCloudClient(GoogleSheetsClientConfig(
        credentials="credentials.json",
        # path to your credentials. 
        # Can be not provided if you are using 
        # environment credentials for Google cloud.
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets"
            # read and write scope
        ]
    ))

    # model that will be used for Q&A task
    model = TokenSearcherPredictor(
        TokenSearcherPredictorConfig(
            device="cpu"
        )
    )

    # Q&A stage
    q_and_a = TokenSearcherQandA(
        predictor=model,
        postprocess=TokenSearcherQandAPostprocessor(
            threshold=0.7
        )
    )


    spreadsheet_id = "1k4pSzvMClric29a_2w-pKjJJQvU2Dq59SrZIy6XUVU4"#"your_spread_sheet_id"
    # can be found in url: https://docs.google.com/spreadsheets/d/***spreadsheet_id***/edit#gid=0

    # create pipeline with described stages
    pipeline = (
        GoogleSheetsRead(client) 
        | ExecuteFunction(get_input_for_q_and_a)
        | q_and_a
        | ExecuteFunction(create_table)
        | AddData({
            "spreadsheet_id": spreadsheet_id,
            "cells_range": "C1"
        }) 
        | GoogleSheetsWrite(client)
    )

    pipeline.run({
        "spreadsheet_id": spreadsheet_id,
        "cells_range": "A2:B2"
    })
    # result should be written to specified spreadsheet