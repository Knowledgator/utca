# Google Spreadsheet

---

## GoogleSpreadsheetClient

Client for actions with Google Spreadsheets

Supported actions:

- create
- read
- write
- append

### GoogleSpreadsheetClientConfig

- credentials: [Dict[str, Any] | str | None]

Object with credentials or path to JSON file.

- scopes: list[str]

Scopes of the Google Cloud api.

---
---

# Actions:

---

## GoogleSpreadsheetCreate


### GoogleSpreadsheetCreateConfig

None

### GoogleSpreadsheetCreateInput

- title: str

Name of the spreadsheet.

- sheets: Optional[list[Sheet]] = None

Description of sheets.

### GoogleSpreadsheetCreateOutput

- spreadsheet_id: str

Spreadsheet ID.

---

## GoogleSpreadsheetRead


### GoogleSpreadsheetReadConfig

- spreadsheet_id: str

Spreadsheet ID (can be found in url: https://docs.google.com/spreadsheets/d/***spreadsheet_id***/edit#gid=0)

- dimension: Dimension (defaults to Dimension.ROWS)

Reading dimension. May be Dimension.ROWS or Dimension.COLUMNS

### GoogleSpreadsheetReadInput

- sheet_name: Optional[str]

Sheet name.

- select_range: Optional[str]

Range of cells provided in A1 notation (Examples: B2:C2, A1).

[!Note] sheet_name and/or select_range should be provided.

### GoogleSpreadsheetReadOutput

table: list[list[Any]]

Table with values.

---

## GoogleSpreadsheetWrite


### GoogleSpreadsheetWriteConfig

- spreadsheet_id: str

Spreadsheet ID (can be found in url: https://docs.google.com/spreadsheets/d/***spreadsheet_id***/edit#gid=0)

- value_input_option: InputOption (defaults to InputOption.USER_ENTERED)

Input option can be InputOption.USER_ENTERED - All inputs treated as input from the user (enabling formatting and formulas), or InputOption.RAW - all inputs as is.

### GoogleSpreadsheetWriteInput

- values: list[list[str]]

Table with values.

- dimension: Dimension (defaults to Dimension.ROWS)

Writing dimension. May be Dimension.ROWS or Dimension.COLUMNS

- sheet_name: Optional[str]

Sheet name.

- select_range: Optional[str]

Range of cells provided in A1 notation (Examples: B2:C2, A1).

[!Note] sheet_name and/or select_range should be provided.

### GoogleSpreadsheetWriteOutput

None

---

## GoogleSpreadsheetAppend


### GoogleSpreadsheetAppendConfig

- spreadsheet_id: str

Spreadsheet ID (can be found in url: https://docs.google.com/spreadsheets/d/***spreadsheet_id***/edit#gid=0)

- value_input_option: InputOption (defaults to InputOption.USER_ENTERED)

Input option can be InputOption.USER_ENTERED - all inputs treated as input from the user (enabling formatting and formulas), or InputOption.RAW - all inputs as is.

- insert_data_option: InsertDataOption (defaults to InsertDataOption.OVERWRITE)

Isert data option can be InsertDataOption.OVERWRITE - will overwrite anything after table, or InsertDataOption.INSERT_ROWS - will insert new rows.

### GoogleSpreadsheetWriteInput

- values: list[list[str]]

Table with values.

- dimension: Dimension (defaults to Dimension.ROWS)

Writing dimension. May be Dimension.ROWS or Dimension.COLUMNS

- sheet_name: Optional[str]

Sheet name.

- select_range: Optional[str]

Range of cells provided in A1 notation (Examples: B2:C2, A1).

[!Note] sheet_name and/or select_range should be provided.

### GoogleSpreadsheetWriteOutput

None

---
---

# Examples

``` python
SAMPLE_SPREADSHEET_ID: str = "spread_sheet_id"
SAMPLE_RANGE_NAME: str = "sheet_name"

cfg = GoogleSpreadsheetClientConfig(
    credentials='credentials.json'
)
cli = GoogleSpreadsheetClient(cfg)


cli.append(GoogleSpreadsheetAppendConfig(
    spreadsheet_id=SAMPLE_SPREADSHEET_ID
)).execute(GoogleSpreadsheetWriteInput(
    sheet_name=SAMPLE_RANGE_NAME,
    values=[['A1', 'A2'], ['E', 'E']],
    dimension=Dimension.ROWS
))

output = cli.read(
    GoogleSpreadsheetReadConfig(
        spreadsheet_id=SAMPLE_SPREADSHEET_ID,
        dimension=Dimension.ROWS
    )
).execute(
    GoogleSpreadsheetReadInput(
        sheet_name=SAMPLE_RANGE_NAME, 
    )
)
```