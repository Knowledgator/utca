from typing import Type, Optional, List, Any

from transformers import AutoModel, AutoTokenizer # type: ignore

from core.executable_level_1.schema import IOModel, Input, Output
from core.executable_level_1.executor import ActionType
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


class TransformersTextEmbedding(
    Task[Input, Output]
):
    """
    Text embedding task
    """
    default_model = "BAAI/bge-large-en-v1.5"
    
    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[List[ActionType]]=None,
        postprocess: Optional[List[ActionType]]=None,
        input_class: Type[Input]=TextEmbeddingInput,
        output_class: Type[Output]=TextEmbeddingOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            predictor (Predictor[Any, Any], optional): Predictor that will be used in task.
                If equals to None, default predictor will be used. Defaults to None.
            
            preprocess (Optional[List[Action[Any, Any]]], optional): Chain of actions executed
                before predictor. If equals to None, default chain will be used. 
                Defaults to None.

                Default chain: 
                    [EmbeddingPreprocessor]

                If default chain is used, EmbeddingPreprocessor will use AutoTokenizer from 
                predictor model.
            
            postprocess (Optional[List[Action[Any, Any]]], optional): Chain of actions executed
                after predictor. If equals to None, default chain will be used. 
                Defaults to None.

                Default chain: 
                    [EmbeddingPostprocessor, ConvertEmbeddingsToNumpyArrays]
            
            input_class (Type[Input], optional): Class for input validation. 
                Defaults to TextEmbeddingInput.
            
            output_class (Type[Output], optional): Class for output validation. 
                Defaults to TextEmbeddingOutput.
            
            name (Optional[str], optional): Name for identification. If equals to None, 
                class name will be used. Defaults to None.
        """
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
                        predictor.config._name_or_path
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