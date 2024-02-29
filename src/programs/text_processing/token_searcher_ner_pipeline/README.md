# Program1

Read PDF, clean text and retrieve entities with labels 'person' and 'framework'.

---

## Stages and pipeline

Program consists from:

- PDF reading stage
- Clean text task
- NER task

### PDF reading stage

To initialize stage use:

``` python
read_pdf = PDFFile().read()
```
 
### Model

Before initializing task we need to initialize models that used by this tasks. In this case both task are using same model.

``` python
model = TokenSearcherModel(TokenSearcherModelConfig(
    device = 'cpu'
))
```

### Clean text task

Clean task will clean text from not informative parts before passing it to NER task.

``` python
clean_task = TokenSearcherTextCleanerTask(
    TokenSearcherTextCleanerConfig(clean=True),
    model
)
```

### NER task

This is the main stage in this program. Result will contain entities that have specified labels (see pipeline below).

``` python
ner_task = TokenSearcherNERTask(
    TokenSearcherNERConfig(
        threshold=0.8
    ),
    model
)
```

### Pipeline

Now we need to create pipeline to combine stages:

``` python
pipeline = (
    read_pdf 
    | ExecuteFunction(get_page) 
    | clean_task 
    | ExecuteFunction(get_ner_input)         
    | AddData({'labels': ['person', 'framework']}) 
    | ner_task
)
```

ExecuteFunction and AddData is used to modify inputs/outputs of the stages for compatibility.

Labels that will be used for classification by NER task provided via this transforamtion:

``` python
AddData({'labels': ['person', 'framework']})
```

---

## Call pipeline

For calling pipeline we need input:

``` python
read_input = PDFReadInput(
    path_to_file='programs/program1/test.pdf'
)
```


To call pipeline use:

``` python
res = Evaluator(pipeline).run(read_input)
```