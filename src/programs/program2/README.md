# Program2

Read Google Spreadsheet table with two columns:

- text;
- question.

Run Q&A task and writes answers in newly created column 'Answer'.

---

## Stages and pipeline

Program consists from:

- Google Spreadsheet reading stage
- Q&A task
- Google Spreadsheet writing stage

### Google Spreadsheet client

To use spreadsheet API we need initialize client:

``` python
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
```

### Google Spreadsheet reading stage

To initialize stage use:

``` python
spreadsheet.read()
```

### Google Spreadsheet writing stage

Similarly to reading stage initialize writing stage:

``` python
spreadsheet.write()
```
 
### Model

Before initializing task we need to initialize model that used by Q&A task.

``` python
model = TokenSearcherModel(
    TokenSearcherModelConfig(
        device='cpu'
    )
)
```

### Q&A task

This is the main stage in this program.

``` python
q_and_a = TokenSearcherQandATask(
    TokenSearcherQandAConfig(
        threshold=0.7
    ),
    model
)
```

Threshold used to filter results by score.

### Pipeline

Now we need to create pipeline to combine stages:

``` python
pipeline = (
    spreadsheet.read() 
    | ExecuteFunction(get_input_for_q_and_a)
    | q_and_a
    | ExecuteFunction(create_table)
    | AddData({
        'spreadsheet_id': spreadsheet_id,
        'select_range': 'C1'
    })
    | spreadsheet.write()
)
```

ExecuteFunction and AddData is used to modify inputs/outputs of the stages for compatibility.

---

## Call pipeline

For calling pipeline we need input:

``` python
read_input = GoogleSpreadsheetReadInput(
    spreadsheet_id=spreadsheet_id,
    select_range='A2:B2'
)
```

Spreadsheet ID can be found in url: https://docs.google.com/spreadsheets/d/***spreadsheet_id***/edit#gid=0

To call pipeline use:

``` python
Evaluator(pipeline).run(read_input)
```

Result will be written to new column with a name 'Answer' of a spreadsheet with spreadsheet_id specified in write configuration.
