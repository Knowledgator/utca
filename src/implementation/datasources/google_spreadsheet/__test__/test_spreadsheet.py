import logging

from implementation.datasources.google_spreadsheet.actions import (
    GoogleSpreadsheetAppend,
    # GoogleSpreadsheetCreate,
    GoogleSpreadsheetRead,
    # GoogleSpreadsheetReadBatch,
    GoogleSpreadsheetSelectRange,
    # GoogleSpreadsheetUpdate,
    # GoogleSpreadsheetUpdateBatch,
    GoogleSpreadsheetWriteRange,
    Dimension,
)
from implementation.datasources.google_spreadsheet.schema import (
    GoogleSpreadsheetClientConfig
)
from implementation.datasources.google_spreadsheet.google_spreadsheet import GoogleSpreadsheetClient

def test_spreadsheet():
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = "1k4pSzvMClric29a_2w-pKjJJQvU2Dq59SrZIy6XUVU4"
    SAMPLE_RANGE_NAME = "Аркуш1"

    cfg = GoogleSpreadsheetClientConfig(credentials='google_spreadsheet/__test__/credentials.json')
    cli = GoogleSpreadsheetClient(cfg)
    # read_batch_action = GoogleSpreadsheetReadBatch(
    #     spreadsheet_id=SAMPLE_SPREADSHEET_ID, 
    #     select_range=[
    #         GoogleSpreadsheetSelectRange(page_name='A1:B1'),
    #         GoogleSpreadsheetSelectRange(page_name='A2:B2')
    #     ],
    #     dimension=Dimension.COLUMNS
    # )
    # print(GoogleSpreadsheetClient('credentials.json').create('HiThere!'))
    # update_action = GoogleSpreadsheetUpdate(
    #     spreadsheet_id=SAMPLE_SPREADSHEET_ID,
    #     select_range=GoogleSpreadsheetWriteRange(
    #         page_name=SAMPLE_RANGE_NAME,
    #         values=[['A1', 'A2']],
    #         dimension=Dimension.COLUMNS
    #     )
    # )
    read_action = GoogleSpreadsheetRead(
        spreadsheet_id=SAMPLE_SPREADSHEET_ID,
        dimension=Dimension.ROWS,
        select_range=GoogleSpreadsheetSelectRange(
            page_name=SAMPLE_RANGE_NAME, 
        )
    )
    # update_batch_action = GoogleSpreadsheetUpdateBatch(
    #     spreadsheet_id=SAMPLE_SPREADSHEET_ID,
    #     select_range=[
    #         GoogleSpreadsheetWriteRange(
    #             select_range='A1',
    #             values=[['Dot']],
    #         ),
    #         GoogleSpreadsheetWriteRange(
    #             select_range='A2:B2',
    #             values=[['A2', 'B2']],
    #         )

    #     ]
    # )
    append_action = GoogleSpreadsheetAppend(
        spreadsheet_id=SAMPLE_SPREADSHEET_ID,
        select_range=GoogleSpreadsheetWriteRange(
            page_name=SAMPLE_RANGE_NAME,
            values=[['A1', 'A2'], ['E', 'E']],
            dimension=Dimension.ROWS
        )
    )


    # print(cli.execute(update_action))
    # print(cli.execute(read_batch_action))
    cli.execute(append_action)
    logging.error(cli.execute(read_action))