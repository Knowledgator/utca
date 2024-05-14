# Google Docs

---

## GoogleDocsClient

Client for actions with Google Docs

Supported actions:

- create
- read
- write

### GoogleDocsClientConfig

- credentials: [Dict[str, Any] | str | None]

Object with credentials or path to JSON file.

- scopes: list[str]

Scopes of the Google Cloud api.

---
---

# Actions:

---

## GoogleDocsCreate


### GoogleDocsCreateConfig

None

### GoogleDocsCreateInput

- title: str

Name of the document.

### GoogleDocsCreateOutput

- document_id: str

Document ID.

---

## GoogleDocsRead


### GoogleDocsReadConfig

None

### GoogleDocsReadInput

- document_id: str

Document ID.

### GoogleDocsReadOutput

- title: str

Name of the document.

- body: Dict[str, Any]

Content of the document.

---

## GoogleDocsWrite


### GoogleDocsWriteConfig

- document_id: str

Document ID (can be found in url: https://docs.google.com/documents/d/***document_id***/edit#gid=0)

### GoogleDocsWriteInput

- action: Dict[str, Any]

Action that will be executed on the text.

### GoogleDocsWriteOutput

None

---
---

# Examples

``` python
DOCUMENT_ID = "document_id"
cli = GoogleDocsClient(
    GoogleDocsClientConfig(credentials='credentials.json')
)
cli.write(GoogleDocsWriteConfig(
    document_id=DOCUMENT_ID,
)).execute(
    GoogleDocsWriteInput(
        action={
            'insertText': {
                'location': {
                    'index': 19,
                },
                'text': '{{template_placeholder}}\n' # '\n' is mandatory for new paragraph
            },

        }
    )
)
cli.read(GoogleDocsReadConfig()).execute(GoogleDocsReadInput(document_id=DOCUMENT_ID))
```