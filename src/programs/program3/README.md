# Program2

Read Google Docs and use Token Searcher model.

---

## Stages and pipeline

Program consists from:

- Google Docs reading stage
- Token Searcher model

### Google Docs client

To use docs API we need initialize client:

``` python
docs = GoogleDocsClient(
    GoogleDocsClientConfig(
        credentials='credentials.json',
        # path to your credentials. 
        # Can be not provided if you are using 
        # environment credentials for Google cloud.
        scopes = [
            "https://www.googleapis.com/auth/documents"
            # read and write scope
        ]
    )
)
```

### Google Spreadsheet reading stage

To initialize stage use:

``` python
docs.read(GoogleDocsReadConfig())
```

### Model

To initialize Token Searcher model use:

``` python
model = TokenSearcherModel(TokenSearcherModelConfig(
    name="knowledgator/UTC-DeBERTa-small"
))
```

### Pipeline

Now we need to create pipeline to combine stages:

``` python
pipeline = (
    docs.read(GoogleDocsReadConfig())
    | ExecuteFunction(get_text)
    | ExecuteFunction(set_prompt)
    | model
)
```

ExecuteFunction is used to modify inputs/outputs of the stages for compatibility.

---

## Call pipeline

For calling pipeline we need input:

``` python
read_input = GoogleDocsReadInput(
    document_id=document_id
)
```

Document ID can be found in url: https://docs.google.com/documents/d/***document_id***/edit#gid=0


To call pipeline use:

``` python
Evaluator(pipeline).run(read_input)
```

Result will be written to new column with a name 'Answer' of a spreadsheet with spreadsheet_id specified in write configuration.