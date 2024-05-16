# Audio processing
from utca.implementation.tasks.audio_processing.text_to_speech.transformers_task.transformers_text_to_speech import (
    TransformersTextToSpeech,
)

from utca.implementation.tasks.audio_processing.speech_to_text.whisper.whisper import (
    WhisperSpeechToText
)

# Image processing
from utca.implementation.tasks.image_processing.charts_and_plots_analysis.transformers_task.transformers_charts_and_plots_analysis import (
    TransformersChartsAndPlotsAnalysis,
    ChartsAndPlotsAnalysisInput,
)
from utca.implementation.tasks.image_processing.charts_and_plots_analysis.transformers_task.actions import (
    ChartsAndPlotsAnalysisPreprocessor,
    ChartsAndPlotsAnalysisPostprocessor,
)

from utca.implementation.tasks.image_processing.documents_q_and_a.transformers_task.transformers_layout_lm import (
    TransformersDocumentQandA,
)

from utca.implementation.tasks.image_processing.image_classification.transformers_task.transformers_image_classification import (
    TransformersImageClassification,
    TransformersImageClassificationInput,
    TransformersImageClassificationOutput,
    TransformersImageClassificationMultilabelOutput,
)
from utca.implementation.tasks.image_processing.image_classification.transformers_task.actions import (
    ImageClassificationPreprocessor,
    ImageClassificationSingleLabelPostprocessor,
    ImageClassificationMultilabelPostprocessor,
)

from utca.implementation.tasks.image_processing.visual_q_and_a.transformers_task.transformers_visual_q_and_a import (
    TransformersVisualQandA,
    TransformersVisualQandAInput,
    TransformersVisualQandAOutput,
    TransformersVisualQandAMultianswerOutput,
)
from utca.implementation.tasks.image_processing.visual_q_and_a.transformers_task.actions import (
    VisualQandAPreprocessor,
    VisualQandAMultianswerPostprocessor,
    VisualQandASingleAnswerPostprocessor,
)

from utca.implementation.tasks.image_processing.object_detection.transformers_task.transformers_object_detection import (
    TransformersObjectDetection,
    TransformersObjectDetectionInput,
    TransformersObjectDetectionOutput,
)
from utca.implementation.tasks.image_processing.object_detection.transformers_task.actions import (
    ObjectDetectionPreprocessor,
    DETRPostprocessor,
)

# Text processing
from utca.implementation.tasks.text_processing.clean_text.token_searcher.token_searcher import (
    TokenSearcherTextCleaner,
    TokenSearcherTextCleanerInput,
    TokenSearcherTextCleanerOutput,
)
from utca.implementation.tasks.text_processing.clean_text.token_searcher.actions import (
    TokenSearcherTextCleanerPreprocessor,
    TokenSearcherTextCleanerPostprocessor,
)

from utca.implementation.tasks.text_processing.embedding.transformers_task.transformers_embedding import (
    TransformersTextEmbedding,
    TextEmbeddingInput, 
    TextEmbeddingOutput,
)
from utca.implementation.tasks.text_processing.embedding.transformers_task.actions import (
    EmbeddingPreprocessor,
    EmbeddingPostprocessor,
    ConvertEmbeddingsToNumpyArrays,
)

from utca.implementation.tasks.text_processing.entity_linking.transformers_task.transformers_entity_linking import (
    TransformersEntityLinking,
    EntityLinkingInput, 
    EntityLinkingOutput,
)
from utca.implementation.tasks.text_processing.entity_linking.transformers_task.actions import (
    EntityLinkingPreprocessor,
    EntityLinkingPostprocessor,
)

from utca.implementation.tasks.text_processing.ner.token_searcher.token_searcher import (
    TokenSearcherNER,
    TokenSearcherNERInput,
    TokenSearcherNEROutput,
)
from utca.implementation.tasks.text_processing.ner.token_searcher.actions import (
    TokenSearcherNERPreprocessor,
    TokenSearcherNERPostprocessor,
)

from utca.implementation.tasks.text_processing.ner.transformers_ner.transformers_token_classification import (
    TransformersTokenClassifier,
    TransformersTokenClassifierOutput,
)
from utca.implementation.tasks.text_processing.ner.transformers_ner.actions import (
    TokenClassifierPostprocessor,
)

from utca.implementation.tasks.text_processing.summarization.transformers_task.transformers_summarization import (
    TransformersTextSummarization,
    SummarizationInput,
    SummarizationOutput,
)
from utca.implementation.tasks.text_processing.summarization.transformers_task.actions import (
    SummarizationPostprocess,
)

from utca.implementation.tasks.text_processing.text_classification.comprehend_it.comprehend_it import (
    ComprehendIt,
)

from utca.implementation.tasks.text_processing.textual_q_and_a.token_searcher.token_searcher import (
    TokenSearcherQandA,
    TokenSearcherQandAInput,
    TokenSearcherQandAOutput,
)
from utca.implementation.tasks.text_processing.textual_q_and_a.token_searcher.actions import (
    TokenSearcherQandAPreprocessor,
    TokenSearcherQandAPostprocessor,
)

from utca.implementation.tasks.text_processing.textual_q_and_a.transformers_task.transformers_q_and_a import (
    TransformersTextualQandA
)
from utca.implementation.tasks.text_processing.textual_q_and_a.transformers_task.actions import (
    QandAPostprocess
)

from utca.implementation.tasks.text_processing.ner.gliner_task.zero_shot_ner import (
    GLiNER,
    GLiNERInput,
    GLiNEROutput,
)
from utca.implementation.tasks.text_processing.ner.gliner_task.actions import (
    GLiNERPreprocessor,
    GLiNERPostprocessor,
)

from utca.implementation.tasks.text_processing.chat.openai.openai_chat import (
    OpenAIChat,
    ChatInput,
    ChatOutput,
)
from utca.implementation.tasks.text_processing.chat.openai.actions import (
    ChatPreprocessor,
    ChatAddContext,
    ChatPostprocessor,
    ChatStreamPostprocessor,
    ChatUpdateContext,
)

from utca.implementation.tasks.text_processing.text_classification.transformers_task.text_classification import (
    TransformersTextClassification
)

__all__ = [
    # Audio processing
    "TransformersTextToSpeech",
    "WhisperSpeechToText",

    # Image processing
    "TransformersChartsAndPlotsAnalysis",
    "ChartsAndPlotsAnalysisInput",
    "ChartsAndPlotsAnalysisPreprocessor",
    "ChartsAndPlotsAnalysisPostprocessor",

    "TransformersDocumentQandA",

    "TransformersImageClassification",
    "TransformersImageClassificationInput",
    "TransformersImageClassificationOutput",
    "TransformersImageClassificationMultilabelOutput",
    "ImageClassificationPreprocessor",
    "ImageClassificationSingleLabelPostprocessor",
    "ImageClassificationMultilabelPostprocessor",

    "TransformersVisualQandA",
    "TransformersVisualQandAInput",
    "TransformersVisualQandAOutput",
    "TransformersVisualQandAMultianswerOutput",
    "VisualQandAPreprocessor",
    "VisualQandAMultianswerPostprocessor",
    "VisualQandASingleAnswerPostprocessor",

    "TransformersObjectDetection",
    "TransformersObjectDetectionInput",
    "TransformersObjectDetectionOutput",
    "ObjectDetectionPreprocessor",
    "DETRPostprocessor",

    # Text processing
    "TokenSearcherTextCleaner",
    "TokenSearcherTextCleanerInput",
    "TokenSearcherTextCleanerOutput",
    "TokenSearcherTextCleanerPreprocessor",
    "TokenSearcherTextCleanerPostprocessor",
    
    "TransformersTextEmbedding",
    "TextEmbeddingInput", 
    "TextEmbeddingOutput",
    "EmbeddingPreprocessor",
    "EmbeddingPostprocessor",
    "ConvertEmbeddingsToNumpyArrays",

    "TransformersEntityLinking",
    "EntityLinkingInput", 
    "EntityLinkingOutput",
    "EntityLinkingPreprocessor",
    "EntityLinkingPostprocessor",

    "TokenSearcherNER",
    "TokenSearcherNERPostprocessor",
    "TokenSearcherNERInput",
    "TokenSearcherNEROutput",
    "TokenSearcherNERPreprocessor",

    "TransformersTokenClassifier",
    "TransformersTokenClassifierOutput",
    "TokenClassifierPostprocessor",

    "TransformersTextSummarization",
    "SummarizationInput",
    "SummarizationOutput",
    "SummarizationPostprocess",

    "ComprehendIt",

    "TokenSearcherQandA",
    "TokenSearcherQandAInput",
    "TokenSearcherQandAOutput",
    "TokenSearcherQandAPreprocessor",
    "TokenSearcherQandAPostprocessor",

    "TransformersTextualQandA",
    "QandAPostprocess",

    "GLiNER",
    "GLiNERInput",
    "GLiNEROutput",
    "GLiNERPreprocessor",
    "GLiNERPostprocessor",

    "OpenAIChat",
    "ChatInput",
    "ChatOutput",
    "ChatPreprocessor",
    "ChatAddContext",
    "ChatPostprocessor",
    "ChatStreamPostprocessor",
    "ChatUpdateContext",

    "TransformersTextClassification"
]