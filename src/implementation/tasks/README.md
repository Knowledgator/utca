# Tasks

Tasks implementations.


## implementation.tasks.clean_text.TokenSearcherTextCleanerTask

Subclass of the NERTask. Used for text cleaning from not informative parts. Use implemintation.models.TokenSearcherModel


### TokenSearcherTextCleanerConfig

- threshold: float (defaults to 0)

Threshold for results scores.

- clean: bool (defaults to False)

Specifies that not informative parts will be excluded from input text and "cleaned_text" attribute will be included. 

### TokenSearcherTextCleanerInput

- threshold: Optional[float]

Threshold for scores of this input results. Has higher priority than config threshold.

- clean: Optional[bool]

Specifies that not informative parts will be excluded from this input text and "cleaned_text" attribute will be included. Has higher priority than config clean.

- text: str

Text for processing.

## TokenSearcherTextCleanerOutput

- outputs: list[core.objects.Entity]

List of not informative parts.

- text: str

Passed text for processing.

- cleaned_text: Optional[str]

Cleaned text.



## implementation.q_and_a.TokenSearcherQandATask

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

## TokenSearcherQandAOutput

- outputs: list[core.objects.Entity]

List of answers.

- text: str

Passed text for processing.

- question: str

Passed question for processing.



## implementation.q_and_a.TokenSearcherNERTask

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

## TokenSearcherNEROutput

- outputs: list[core.objects.ClassifiedEntity]

List of classified entities.

- text: str

Passed text for processing.