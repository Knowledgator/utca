# TokenSearcherModel

Implemintation of the Token Searcher model.

Is subclass of the core.TransformersPipeline and core.PromptModel.


### TokenSearcherModelConfig

- name: str (defaults to "knowledgator/UTC-DeBERTa-small")

Name of the model or model directory.

- device: [int | str | torch.device]

Defines the device (e.g., "cpu", "cuda:1", "mps", or a GPU ordinal rank like 1) on which this pipeline will be allocated.

- device_map: [str | Dict[str, Union[int, str, torch.device]]]

Sent directly as model_kwargs (just a simpler shortcut). When accelerate library is present, set device_map="auto" to compute the most optimized device_map automatically (see here for more information).

- kwargs: Dict[str, Any]

Additional keyword arguments passed along to the specific pipeline init (see the documentation for the corresponding pipeline class for possible values).

### TokenSearcherModelInput

- inputs: list[str]

Prepared prompts for processing.

### TokenSearcherModelOutput

- inputs: list[str]

Passed inputs.

- outputs: list[list[Dict[str, Any]]]

List with coresponding lists of entities to inputs.



### Examples

``` python
cfg = TokenSearcherModelConfig()

model = TokenSearcherModel(cfg)
ouput = model.execute({
    "inputs": [(
        "Identify organizations mentioned in the text:"
        " The National Aeronautics and Space Administration"
        " (NASA) is an independent agency of the U.S. federal"
        " government responsible for the civilian space program,"
        " as well as aeronautics and space research."
    )]
})
```

---