import logging

from implementation.apis.google_cloud.client import GoogleCloudClient
from implementation.datasources.google_spreadsheet.schema import (
    GoogleSpreadsheetClientConfig,
    Dimension
)
from implementation.datasources.google_spreadsheet.actions import (
    GoogleSpreadsheetAppend,
    GoogleSpreadsheetRead
)

def test_spreadsheet():
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = "..."
    SAMPLE_RANGE_NAME = "Sheet1"

    cfg = GoogleSpreadsheetClientConfig(
        credentials='__test__/credentials.json'
    )
    client = GoogleCloudClient(cfg)


    GoogleSpreadsheetAppend(client).execute({
        "spreadsheet_id": SAMPLE_SPREADSHEET_ID,
        "sheet_name": SAMPLE_RANGE_NAME,
        "table": [['A1', 'A2'], ['E', 'E']],
        "dimension": Dimension.ROWS
    })

    logging.error(
        GoogleSpreadsheetRead(client).execute({
            "spreadsheet_id": SAMPLE_SPREADSHEET_ID,
            "sheet_name": SAMPLE_RANGE_NAME, 
        })
    )