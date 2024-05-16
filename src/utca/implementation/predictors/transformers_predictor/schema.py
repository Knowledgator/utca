from typing import Any, Dict, List, Callable, Optional, Union

from pydantic import ConfigDict
from transformers import ( # type: ignore
    PreTrainedModel,
    TFPreTrainedModel,
    PretrainedConfig,
    PreTrainedTokenizer,
)
from transformers.image_processing_utils import ( # type: ignore
    BaseImageProcessor
)
from PIL import Image
import torch

from utca.core.executable_level_1.schema import IOModel, Config

class TransformersModelConfig(Config):
    """
    Transformers model configuration

    Arguments:
        model (Union[PreTrainedModel, TFPreTrainedModel]): Transformers model that wil be used.

        kwargs (Optional[Dict[str, Any]], optional): Extra model parameters.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    model: Union[PreTrainedModel, TFPreTrainedModel]
    kwargs: Optional[Dict[str, Any]]=None


    def get_kwargs(self) -> Dict[str, Any]:
        return self.kwargs or {}


class TransformersPipelineConfig(Config):
    """
    Transformers pipeline configuration

    Arguments:
        task (Optional[str], optional):  The task defining which pipeline will be returned. 
            Defaults to None. Currently accepted tasks are:
                "audio-classification": will return a AudioClassificationPipeline.
                "automatic-speech-recognition": will return a AutomaticSpeechRecognitionPipeline.
                "conversational": will return a ConversationalPipeline.
                "depth-estimation": will return a DepthEstimationPipeline.
                "document-question-answering": will return a DocumentQuestionAnsweringPipeline.
                "feature-extraction": will return a FeatureExtractionPipeline.
                "fill-mask": will return a FillMaskPipeline:.
                "image-classification": will return a ImageClassificationPipeline.
                "image-feature-extraction": will return an ImageFeatureExtractionPipeline.
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
        
        model (Optional[Union[str, PreTrainedModel, TFPreTrainedModel]], optional): The model 
            that will be used by the pipeline to make predictions. This can be a model 
            identifier or an actual instance of a pretrained model inheriting from 
            PreTrainedModel (for PyTorch) or TFPreTrainedModel (for TensorFlow). 
            Defaults to None.

        config (Optional[Union[str, PretrainedConfig]], optional): The configuration 
            that will be used by the pipeline to instantiate the model. This can be a model 
            identifier or an actual pretrained model configuration inheriting from 
            PretrainedConfig. Defaults to None.
        
        tokenizer (Optional[Union[str, PreTrainedTokenizer]], optional): The tokenizer 
            that will be used by the pipeline to encode data for the model. This can be 
            a model identifier or an actual pretrained tokenizer inheriting from 
            PreTrainedTokenizer. Defaults to None.
        
        feature_extractor (Optional[Any], optional): The feature extractor that will be used
            by the pipeline to encode data for the model. This can be a model identifier 
            or an actual pretrained feature extractor inheriting from 
            PreTrainedFeatureExtractor. Defaults to None.
        
            Feature extractors are used for non-NLP models, such as Speech or Vision models as well
            as multi-modal models. Multi-modal models will also require a tokenizer to be passed.

            If not provided, the default feature extractor for the given model will be loaded
            (if it is a string). If model is not specified or not a string, then the default 
            feature extractor for config is loaded (if it is a string). However, if config
            is also not given or not a string, then the default feature extractor for the given
            task will be loaded.

        image_processor (Optional[Union[str, BaseImageProcessor]], optional): Defaults to None.

        framework (Optional[str], optional): The framework to use, either "pt" for PyTorch 
            or "tf" for TensorFlow. The specified framework must be installed. Defaults to None.

            If no framework is specified, will default to the one currently installed. 
            If no framework is specified and both frameworks are installed, will default 
            to the framework of the model, or to PyTorch if no model is provided.
    
        revision (Optional[str], optional): When passing a task name or a string model identifier: 
            The specific model version to use. It can be a branch name, a tag name, or a commit id,
            since we use a git-based system for storing models and other artifacts on huggingface.co,
            so revision can be any identifier allowed by git.

            If equals to None, "main" will be used. Defaults to None.

        use_fast (bool, optional): Whether or not to use a Fast tokenizer if possible (a PreTrainedTokenizerFast).
            Defaults to True.

        token (Optional[Union[str, bool]], optional): The token to use as HTTP bearer authorization for 
            remote files. If True, will use the token generated when running huggingface-cli login 
            (stored in ~/.huggingface). Defaults to None.

        device (Optional[Union[int, str, torch.device]], optional): Defines the device (e.g., "cpu", "cuda:1", "mps", 
            or a GPU ordinal rank like 1) on which this pipeline will be allocated. Defaults to None.

        device_map (Optional[Union[str, Dict[str, Union[int, str, torch.device]]]], optional): Sent directly as model_kwargs
            (just a simpler shortcut). When accelerate library is present, set device_map="auto" to compute the most optimized
            device_map automatically (see https://huggingface.co/docs/accelerate/main/en/package_reference/big_modeling#accelerate.cpu_offload
            for more information). Defaults to None.

        torch_dtype (Optional[Union[str, torch.dtype]], optional): Sent directly as model_kwargs (just a simpler shortcut)
            to use the available precision for this model (torch.float16, torch.bfloat16, … or "auto").
            Defaults to None.
        
        trust_remote_code (bool, optional): Whether or not to allow for custom code defined on the Hub in their own modeling,
            configuration, tokenization or even pipeline files. This option should only be set to True for repositories
            you trust and in which you have read the code, as it will execute code present on the Hub on your local machine.
            Defaults to False.
        
        model_kwargs (Optional[Dict[str, Any]], optional): Additional dictionary of keyword arguments passed along to the
            model’s from_pretrained(..., **model_kwargs) function. Defaults to None.
        
        pipeline_class (Optional[Any], optional): Defaults to None.
        
        kwargs (Optional[Dict[str, Any]], optional): Additional keyword arguments passed along to the specific pipeline 
            init (see the documentation for the corresponding pipeline class for possible values). Defaults to None.
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True, 
        protected_namespaces=()
    )

    task: Optional[str]=None
    model: Optional[Union[
        str,
        PreTrainedModel,
        TFPreTrainedModel
    ]]=None
    config: Optional[Union[
        str,
        PretrainedConfig
    ]]=None
    tokenizer: Optional[Union[
        str,
        PreTrainedTokenizer
    ]]=None
    feature_extractor: Optional[Any]=None
    image_processor: Optional[Union[
        str, 
        BaseImageProcessor
    ]]=None
    framework: Optional[str]=None
    revision: Optional[str]=None
    use_fast: bool=True
    token: Optional[Union[str, bool]]=None
    device: Optional[Union[int, str, torch.device]]=None
    device_map: Optional[Union[
        str, 
        Dict[str, Union[int, str, torch.device]
    ]]]=None
    torch_dtype: Optional[Union[str, torch.dtype]]=None
    trust_remote_code: bool=False
    model_kwargs: Optional[Dict[str, Any]]=None
    pipeline_class: Optional[Any]=None
    kwargs: Optional[Dict[str, Any]]=None


    @property
    def pipeline_config(self) -> Dict[str, Any]:
        tmp = self.model_dump(exclude={"kwargs"})
        if self.kwargs:
            tmp.update(self.kwargs)
        return tmp


class TransformersImageClassificationModelInput(IOModel):
    pixel_values: Any


class TransformersTextToSpeechInput(IOModel):
    text_inputs: str


class TransformersTextToSpeechOutput(IOModel):
    audio: Any
    sampling_rate: int


class TransformersChartsAndPlotsModelInput(IOModel):
    flattened_patches: Any
    attention_mask: Any


class TransformersVisualQandAInput(IOModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
        
    image: Image.Image
    question: str


class TransformersImageModelInput(IOModel):
    input_ids: Any
    token_type_ids: Any
    attention_mask: Any
    pixel_values: Any
    pixel_mask: Any


class TransformersEmbeddingInput(IOModel):
    encodings: Any


class TransformersEmbeddingOutput(IOModel):
    last_hidden_state: Any


class TransformersEntityLinkingInput(IOModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    encodings: Any
    num_beams: int
    num_return_sequences: int
    prefix_allowed_tokens_fn: Callable[
        [torch.Tensor, int], List[int]
    ]


class TransformersEntityLinkingOutput(IOModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sequences: Any
    sequences_scores: Optional[Any]=None


class TransformersTextualQandAInput(IOModel):
    question: str
    context: str


class TransformersTextualQandAOutput(IOModel):
    answer: Optional[str]=None
    score: float=0.


class TransformersBasicInput(IOModel):
    inputs: Any


class TransformersLogitsOutput(IOModel):
    logits: Any


class TransformersBasicOutput(IOModel):
    output: Any


class TransformersDETROutput(IOModel):
    pred_boxes: Any
    logits: Any