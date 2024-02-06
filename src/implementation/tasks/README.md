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

### TokenSearcherTextCleanerOutput

- outputs: list[core.objects.Entity]

List of not informative parts.

- text: str

Passed text for processing.

- cleaned_text: Optional[str]

Cleaned text.



### Examples

``` python
cfg = TokenSearcherTextCleanerConfig()
task = TokenSearcherTextCleanerTask(
    cfg, TokenSearcherModel(TokenSearcherModelConfig(
        name="knowledgator/UTC-DeBERTa-small"
    ))
)

text = "The mechanism of action was characterized using native mass spectrometry, the thermal shift-binding assay, and enzymatic kinetic studies (Figure ). In the native mass spectrometry binding assay, compound 23R showed dose-dependent binding to SARS-CoV-2 Mpro, similar to the positive control GC376, with a binding stoichiometry of one drug per monomer (Figure A). Similarly, compound 23R showed dose-dependent stabilization of the SARS-CoV-2 Mpro in the thermal shift binding assay with an apparent Kd value of 9.43 μM, a 9.3-fold decrease compared to ML188 (1) (Figure B). In the enzymatic kinetic studies, 23R was shown to be a noncovalent inhibitor with a Ki value of 0.07 μM (Figure C, D top and middle panels). In comparison, the Ki for the parent compound ML188 (1) is 2.29 μM. The Lineweaver–Burk or double-reciprocal plot with different compound concentrations yielded an intercept at the Y-axis, suggesting that 23R is a competitive inhibitor similar to ML188 (1) (Figure C, D bottom panel). Buy our T-shirts for the lowerst prices you can find!!!  Overall, the enzymatic kinetic studies confirmed that compound 23R is a noncovalent inhibitor of SARS-CoV-2 Mpro."
output = task.execute({
    "text": text,
    "clean": True
})
```


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