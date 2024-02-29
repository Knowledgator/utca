from typing import Dict, Any

from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.actions import (
    ExecuteFunction,
    AddData,
    OneToOne
)
from implementation.apis.google_cloud.client import GoogleCloudClient
from implementation.datasources.google_spreadsheet.schema import (
    GoogleSpreadsheetClientConfig,
)
from implementation.datasources.google_spreadsheet.actions import (
    GoogleSpreadsheetRead,
    GoogleSpreadsheetWrite
)
from implementation.datasources.google_spreadsheet.schema import (
    Dimension
)
from implementation.predictors.token_searcher.predictor import (
    TokenSearcherPredictor, TokenSearcherPredictorConfig
)
from implementation.tasks.text_processing.textual_q_and_a.token_searcher.token_searcher import (
    TokenSearcherQandATask
)
from implementation.tasks.text_processing.textual_q_and_a.token_searcher.actions import (
    TokenSearcherQandAPostprocessor,
    TokenSearcherQandAPostprocessorConfig
)

def get_input_for_q_and_a(input: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'text': input['table'][0][0],
        'question': input['table'][0][1]
    }


def create_table(input: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'table': [
            [f'Answer {i+1}', input['output'][i]['span']]
            for i in range(len(input['output']))
        ],
        'dimension': Dimension.COLUMNS
    }


if __name__ == '__main__':
    # Google Spreadsheet client
    client = GoogleCloudClient(GoogleSpreadsheetClientConfig(
        credentials='credentials.json',
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
            device='cpu'
        )
    )

    # Q&A stage
    q_and_a = TokenSearcherQandATask(
        predictor=model,
        postprocess=[TokenSearcherQandAPostprocessor(
            TokenSearcherQandAPostprocessorConfig(
                threshold=0.7
            )
        )]
    )


    spreadsheet_id = '1k4pSzvMClric29a_2w-pKjJJQvU2Dq59SrZIy6XUVU4'#'your_spread_sheet_id'
    # can be found in url: https://docs.google.com/spreadsheets/d/***spreadsheet_id***/edit#gid=0

    # create pipeline with described stages
    pipeline = (
        GoogleSpreadsheetRead(client) 
        | OneToOne(ExecuteFunction)(get_input_for_q_and_a)
        | q_and_a
        | OneToOne(ExecuteFunction)(create_table)
        | AddData({
            'spreadsheet_id': spreadsheet_id,
            'cells_range': 'C1'
        }) 
        | GoogleSpreadsheetWrite(client)
    )

    Evaluator(pipeline).run_program({
        "spreadsheet_id": spreadsheet_id,
        "cells_range": "A2:B2"
    })
    # result should be written to specified spreadsheet