# Models

Classes used for AI models abstractions.

---

## Model

Abstract subclass of the Executable and base class of the models.


### ModelConfig

Configurations for model.

### ModelInput

Type of the model input will be used for validation input and invokation of the main logic.

### ModelOutput

Type of the model output will be used for validation output. Can be used for returning value.

Returning value can be:

- Dict[str, Any];
- Transformable;
- ModelOutput

---

## PromptModel

Abstract class of models that use prompts.

---