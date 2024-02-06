# Clean Text Tasks

Tasks for text cleaning.

---

## TokenSearcherTextCleanerTask

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

---