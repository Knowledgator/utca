# utca

# Models

Classes used for AI models abstractions.



## class core.Model

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



## class core.PromptModel

Abstract class of models that use prompts.



## class core.TransformersPipeline

Abstract subclass of the Model.

Used for transformers.Pipeline abstraction.


### TransformersPipelineConfig

- task: str

The task defining which pipeline will be returned. Currently accepted tasks are:
"audio-classification": will return a AudioClassificationPipeline.
"automatic-speech-recognition": will return a AutomaticSpeechRecognitionPipeline.
"conversational": will return a ConversationalPipeline.
"depth-estimation": will return a DepthEstimationPipeline.
"document-question-answering": will return a DocumentQuestionAnsweringPipeline.
"feature-extraction": will return a FeatureExtractionPipeline.
"fill-mask": will return a FillMaskPipeline:.
"image-classification": will return a ImageClassificationPipeline.
"image-segmentation": will return a ImageSegmentationPipeline.
"image-to-image": will return a ImageToImagePipeline.
"image-to-text": will return a ImageToTextPipeline.
"mask-generation": will return a MaskGenerationPipeline.
"object-detection": will return a ObjectDetectionPipeline.
"question-answering": will return a QuestionAnsweringPipeline.
"summarization": will return a SummarizationPipeline.
"table-question-answering": will return a TableQuestionAnsweringPipeline.
"text2text-generation": will return a Text2TextGenerationPipeline.
"text-classification" (alias "sentiment-analysis" available): will return a TextClassificationPipeline.
"text-generation": will return a TextGenerationPipeline:.
"text-to-audio" (alias "text-to-speech" available): will return a TextToAudioPipeline:.
"token-classification" (alias "ner" available): will return a TokenClassificationPipeline.
"translation": will return a TranslationPipeline.
"translation_xx_to_yy": will return a TranslationPipeline.
"video-classification": will return a VideoClassificationPipeline.
"visual-question-answering": will return a VisualQuestionAnsweringPipeline.
"zero-shot-classification": will return a ZeroShotClassificationPipeline.
"zero-shot-image-classification": will return a ZeroShotImageClassificationPipeline.
"zero-shot-audio-classification": will return a ZeroShotAudioClassificationPipeline.
"zero-shot-object-detection": will return a ZeroShotObjectDetectionPipeline.
model (str or PreTrainedModel or TFPreTrainedModel, optional) — The model that will be used by the pipeline to make predictions. This can be a model identifier or an actual instance of a pretrained model inheriting from PreTrainedModel (for PyTorch) or TFPreTrainedModel (for TensorFlow).
If not provided, the default for the task will be loaded.

- config [str | PretrainedConfig]

The configuration that will be used by the pipeline to instantiate the model. This can be a model identifier or an actual pretrained model configuration inheriting from PretrainedConfig.
If not provided, the default configuration file for the requested model will be used. That means that if model is given, its default configuration will be used. However, if model is not supplied, this task’s default model’s config is used instead.

- tokenizer [str | PreTrainedTokenizer]

The tokenizer that will be used by the pipeline to encode data for the model. This can be a model identifier or an actual pretrained tokenizer inheriting from PreTrainedTokenizer.
If not provided, the default tokenizer for the given model will be loaded (if it is a string). If model is not specified or not a string, then the default tokenizer for config is loaded (if it is a string). However, if config is also not given or not a string, then the default tokenizer for the given task will be loaded.

- feature_extractor [str | PreTrainedFeatureExtractor]

The feature extractor that will be used by the pipeline to encode data for the model. This can be a model identifier or an actual pretrained feature extractor inheriting from PreTrainedFeatureExtractor.
Feature extractors are used for non-NLP models, such as Speech or Vision models as well as multi-modal models. Multi-modal models will also require a tokenizer to be passed.

If not provided, the default feature extractor for the given model will be loaded (if it is a string). If model is not specified or not a string, then the default feature extractor for config is loaded (if it is a string). However, if config is also not given or not a string, then the default feature extractor for the given task will be loaded.

- framework: str

The framework to use, either "pt" for PyTorch or "tf" for TensorFlow. The specified framework must be installed.
If no framework is specified, will default to the one currently installed. If no framework is specified and both frameworks are installed, will default to the framework of the model, or to PyTorch if no model is provided.

- revision: str (defaults to "main")

When passing a task name or a string model identifier: The specific model version to use. It can be a branch name, a tag name, or a commit id, since we use a git-based system for storing models and other artifacts on huggingface.co, so revision can be any identifier allowed by git.

- use_fast: bool (defaults to True)

Whether or not to use a Fast tokenizer if possible (a PreTrainedTokenizerFast).
use_auth_token (str or bool, optional) — The token to use as HTTP bearer authorization for remote files. If True, will use the token generated when running huggingface-cli login (stored in ~/.huggingface).

- device: [int | str | torch.device]

Defines the device (e.g., "cpu", "cuda:1", "mps", or a GPU ordinal rank like 1) on which this pipeline will be allocated.

- device_map: [str | Dict[str, Union[int, str, torch.device]]]

Sent directly as model_kwargs (just a simpler shortcut). When accelerate library is present, set device_map="auto" to compute the most optimized device_map automatically (see here for more information).

Do not use device_map AND device at the same time as they will conflict

- torch_dtype: [str | torch.dtype]

Sent directly as model_kwargs (just a simpler shortcut) to use the available precision for this model (torch.float16, torch.bfloat16, … or "auto").

- trust_remote_code: [bool] (defaults to False)

Whether or not to allow for custom code defined on the Hub in their own modeling, configuration, tokenization or even pipeline files. This option should only be set to True for repositories you trust and in which you have read the code, as it will execute code present on the Hub on your local machine.

- model_kwargs: Dict[str, Any]

Additional dictionary of keyword arguments passed along to the model’s from_pretrained(..., **model_kwargs) function.

- kwargs: Dict[str, Any]

Additional keyword arguments passed along to the specific pipeline init (see the documentation for the corresponding pipeline class for possible values).



## class implemintation.models.TokenSearcherModel

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



# Tasks

## core.Task

Abstract subclass of the Executable and base class of the tasks. Use Models


## core.NERTask

Subclass of the Task. Abstraction for NER tasks.



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


# core.Objects

## Entity

- span: str

Text of the entity.

- start: int

Start postition in a text.

- end: int

End postition in a text.



## ClassifiedEntity

- span: str

Text of the entity.

- start: int

Start postition in a text.

- end: int

End postition in a text.

- entity: str

Class of the entity.