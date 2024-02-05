import logging

from implementation.datasources.google_spreadsheet.actions import (
    GoogleSpreadsheetReadInput,
    GoogleSpreadsheetWriteInput,
)
from implementation.datasources.google_spreadsheet.schema import (
    GoogleSpreadsheetClientConfig,
    GoogleSpreadsheetReadConfig,
    GoogleSpreadsheetAppendConfig,
    Dimension
)
from implementation.datasources.google_spreadsheet.google_spreadsheet import GoogleSpreadsheetClient

def test_spreadsheet():
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = "1k4pSzvMClric29a_2w-pKjJJQvU2Dq59SrZIy6XUVU4"
    SAMPLE_RANGE_NAME = "Аркуш1"

    cfg = GoogleSpreadsheetClientConfig(
        credentials='__test__/credentials.json'
    )
    cli = GoogleSpreadsheetClient(cfg)


    cli.append(GoogleSpreadsheetAppendConfig(
        spreadsheet_id=SAMPLE_SPREADSHEET_ID
    )).execute(GoogleSpreadsheetWriteInput(
        page_name=SAMPLE_RANGE_NAME,
        values=[['A1', 'A2'], ['E', 'E']],
        dimension=Dimension.ROWS
    ))

    logging.error(cli.read(
        GoogleSpreadsheetReadConfig(
            spreadsheet_id=SAMPLE_SPREADSHEET_ID,
            dimension=Dimension.ROWS
        )
    ).execute(
        GoogleSpreadsheetReadInput(
            page_name=SAMPLE_RANGE_NAME, 
        )
    ))