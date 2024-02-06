# NER Tasks

NER tasks.

---

## TokenSearcherNERTask

Subclass of the NERTask. Used for NER tasks. Use implemintation.models.TokenSearcherModel


### TokenSearcherNERConfig

- threshold: float (defaults to 0)

Threshold for results scores.

- sent_batch: int (defaults to 10)

Amount of sentences processed in a batch

### TokenSearcherNERInput

- threshold: Optional[float]

Threshold for scores of this input results. Has higher priority than config threshold.

- text: str

Text for processing.

- labels: list[str]

Classification labels.

### TokenSearcherNEROutput

- outputs: list[core.objects.ClassifiedEntity]

List of classified entities.

- text: str

Passed text for processing.



### Examples

``` python
cfg = TokenSearcherNERConfig()
task = TokenSearcherNERTask(
    cfg, TokenSearcherModel(TokenSearcherModelConfig(
        name="knowledgator/UTC-DeBERTa-small"
    ))
)

output = task.execute({
    "text": "Dr. Paul Hammond, a renowned neurologist at Johns Hopkins University, has recently published a paper in the prestigious journal \"Nature Neuroscience\". \nHis research focuses on a rare genetic mutation, found in less than 0.01% of the population, that appears to prevent the development of Alzheimer's disease. Collaborating with researchers at the University of California, San Francisco, the team is now working to understand the mechanism by which this mutation confers its protective effect. \nFunded by the National Institutes of Health, their research could potentially open new avenues for Alzheimer's treatment.",
    "labels": [
        "scientist",
        "university",
        "city"
    ],
})
```

---