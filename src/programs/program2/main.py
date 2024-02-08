from typing import Dict, Any

from core.executable_level_1.eval import Evaluator
from core.executable_level_1.schema import (
    ExecuteFunction,
    AddData
)
from implementation.datasources.google_spreadsheet.google_spreadsheet import (
    GoogleSpreadsheetClient, 
    GoogleSpreadsheetClientConfig,
    GoogleSpreadsheetReadConfig,
    GoogleSpreadsheetReadInput,
    GoogleSpreadsheetWriteConfig,
)
from implementation.datasources.google_spreadsheet.schema import (
    Dimension
)
from implementation.models.token_searcher.model import (
    TokenSearcherModel, TokenSearcherModelConfig
)
from implementation.tasks.q_and_a.token_searcher import (
    TokenSearcherQandAConfig, TokenSearcherQandATask
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
    spreadsheet = GoogleSpreadsheetClient(
        GoogleSpreadsheetClientConfig(
            credentials='credentials.json',
            # path to your credentials. 
            # Can be not provided if you are using 
            # environment credentials for Google cloud.
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets"
                # read and write scope
            ]
        )
    )

    # model that will be used for Q&A task
    model = TokenSearcherModel(
        TokenSearcherModelConfig(
            name="knowledgator/UTC-DeBERTa-small"
        )
    )

    # Q&A stage
    q_and_a = TokenSearcherQandATask(
        TokenSearcherQandAConfig(
            threshold=0.7
        ),
        model
    )

    spreadsheet_id = '1k4pSzvMClric29a_2w-pKjJJQvU2Dq59SrZIy6XUVU4'#'your_spread_sheet_id'
    # can be found in url: https://docs.google.com/spreadsheets/d/***spreadsheet_id***/edit#gid=0
    
    # create pipeline with described stages
    pipeline = (
        spreadsheet.read(
            GoogleSpreadsheetReadConfig(
                spreadsheet_id=spreadsheet_id
            )
        ) 
        | ExecuteFunction(get_input_for_q_and_a)
        | q_and_a
        | ExecuteFunction(create_table)
        | AddData({'select_range': 'C1'}) 
        | spreadsheet.write(
            GoogleSpreadsheetWriteConfig(
                spreadsheet_id=spreadsheet_id
            )
        )
    )

    read_input = GoogleSpreadsheetReadInput(
        select_range='A2:B2'
    )
    Evaluator(pipeline).run(read_input)
    # result should be written to specified spreadsheet