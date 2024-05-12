# Q&A Tasks

Q&A tasks.

---

## TokenSearcherQandATask

Subclass of the NERTask. Used for Q and A tasks. Use implemintation.models.TokenSearcherModel


### TokenSearcherQandAConfig

- threshold: float (defaults to 0)

Threshold for results scores.

### TokenSearcherQandAInput

- threshold: Optional[float]

Threshold for scores of this input results. Has higher priority than config threshold.

- text: str

Text for processing.

- question: str

Question for processing.

### TokenSearcherQandAOutput

- outputs: list[core.objects.Entity]

List of answers.

- text: str

Passed text for processing.

- question: str

Passed question for processing.



### Examples

``` python
cfg = TokenSearcherQandAConfig()

task = TokenSearcherQandATask(
    cfg, TokenSearcherModel(TokenSearcherModelConfig(
        name="knowledgator/UTC-DeBERTa-small"
    ))
)

output = task.execute({
    "question": "Who are the founders of Microsoft?",
    "text": "Microsoft was founded by Bill Gates and Paul Allen on April 4, 1975 to develop and sell BASIC interpreters for the Altair 8800. During his career at Microsoft, Gates held the positions of chairman, chief executive officer, president and chief software architect, while also being the largest individual shareholder until May 2014."
})
```

---