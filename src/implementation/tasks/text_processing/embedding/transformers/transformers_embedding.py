from typing import Type, Optional, List, Any

from transformers import AutoModel, AutoTokenizer # type: ignore

from core.executable_level_1.schema import IOModel
from core.executable_level_1.actions import Action
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.task import Task
from implementation.predictors.transformers.transformers_model import (
    TransformersModel,
    TransformersModelConfig
)
from implementation.predictors.transformers.schema import (
    TransformersEmbeddingInput,
    TransformersEmbeddingOutput,
)
from implementation.tasks.text_processing.embedding.transformers.actions import (
    EmbeddingPreprocessor,
    EmbeddingPostprocessor,
    ConvertEmbeddingsToNumpyArrays,
)

class TextEmbeddingInput(IOModel):
    texts: List[str]


class TextEmbeddingOutput(IOModel):
    embeddings: Any


class TextEmbedding(
    Task[
        TextEmbeddingInput, 
        TextEmbeddingOutput,
    ]
):
    default_model = "BAAI/bge-large-en-v1.5"
    
    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[List[Action[Any, Any]]]=None,
        postprocess: Optional[List[Action[Any, Any]]]=None,
        input_class: Type[TextEmbeddingInput]=TextEmbeddingInput,
        output_class: Type[TextEmbeddingOutput]=TextEmbeddingOutput,
        name: Optional[str]=None,
    ) -> None:
        

        if not predictor:
            model = AutoModel.from_pretrained(self.default_model) # type: ignore
            predictor = TransformersModel(
                TransformersModelConfig(
                    model=model # type: ignore
                ),
                input_class=TransformersEmbeddingInput,
                output_class=TransformersEmbeddingOutput,
            )

        super().__init__(
            predictor=predictor,
            preprocess=preprocess or [
                EmbeddingPreprocessor(
                    tokenizer=AutoTokenizer.from_pretrained( # type: ignore 
                        self.default_model
                    )
                )
            ],
            postprocess=postprocess or [
                EmbeddingPostprocessor(),
                ConvertEmbeddingsToNumpyArrays()    
            ],
            input_class=input_class, 
            output_class=output_class,
            name=name,
        )