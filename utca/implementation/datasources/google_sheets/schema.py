from enum import Enum

from utca.implementation.apis.google_cloud.schema import (
    GoogleCloudClientConfig,
)

class GoogleSheetsClientConfig(GoogleCloudClientConfig):
    """
    Google Spreadsheets default configuration

    Args:
        scopes (List[str]): Access scopes. Defaults to 
            ["https://www.googleapis.com/auth/spreadsheets"]
            (Read and write acess to all spreadsheets).
        
        service (str): Service name. Defaults to "sheets" (Google Spreadsheets service).
        
        version (str): API version. Defaults to "v4".
    """
    scopes: list[str] = [
        "https://www.googleapis.com/auth/spreadsheets"
    ]
    service: str = "sheets"
    version: str = "v4"


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
    OVERWRITE = 'OVERWRITE'
    """
    Overwrite anything after table
    """
    INSERT_ROWS = 'INSERT_ROWS'
    """
    Insert new rows
    """