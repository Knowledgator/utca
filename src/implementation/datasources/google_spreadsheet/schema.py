from enum import Enum

from implementation.apis.google_cloud.schema import (
    GoogleCloudClientConfig,
)

class GoogleSpreadsheetClientConfig(GoogleCloudClientConfig):
    """
    Google Spreadsheets default configuration
    """
    scopes: list[str] = [
        "https://www.googleapis.com/auth/spreadsheets"
    ]
    """
    Read and write acess to all spreadsheets
    """
    service: str="sheets"
    """
    Google Spreadsheets service
    """
    version: str="v4"
    """
    API version
    """


class Dimension(Enum):
    """
    Specify major dimension(i.e. what outer list represents)
    """
    ROWS = 'ROWS'
    COLUMNS = 'COLUMNS'


class InputOption(Enum):
    """
    Specify how input data should be formatted
    """
    RAW = 'RAW'
    """
    Inputs as is
    """
    USER_ENTERED = 'USER_ENTERED'
    """
    All inputs treated as input from the user (enabling formatting and formulas)
    """

class InsertDataOption(Enum):
    """
    How data should be append to table
    """
    INSERT_ROWS = 'INSERT_ROWS'
    """
    Overwrite anything after table
    """
    OVERWRITE = 'OVERWRITE'
    """
    Insert new rows
    """