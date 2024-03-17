from typing import Type, Optional, List, Any

from transformers import AutoModel, AutoTokenizer # type: ignore

from core.executable_level_1.actions import (
    Action, ActionInput, ActionOutput
)
from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import (
    PredictorInput, PredictorOutput
)
from core.predictor_level_2.schema import (
    PredictorInput,
    PredictorOutput
)
from core.task_level_3.task import Task
from core.task_level_3.schema import (
    Input, Output,
)
from implementation.predictors.transformers.transformers_model import (
    TransformersModel,
    TransformersModelConfig
)
from implementation.tasks.text_processing.embedding.transformers.actions import (
    EmbeddingPreprocessor,
    EmbeddingPreprocessorConfig,
    EmbeddingPostprocessor,
    ConvertEmbeddingsToNumpyArrays,
)

class TextEmbeddingInput(Input):
    texts: List[str]


class TextEmbeddingOutput(Output):
    embeddings: Any


class ModelInput(PredictorInput):
    encodings: Any


class ModelOutput(PredictorOutput):
    last_hidden_state: Any


class TextEmbeddingTask(
    Task[
        TextEmbeddingInput, 
        TextEmbeddingOutput,
    ]
):
    default_model = "BAAI/bge-large-en-v1.5"
    
    def __init__(
        self,
        *,
        predictor: Optional[Predictor[
            PredictorInput, 
            PredictorOutput
        ]]=None,
        preprocess: Optional[List[Action[ActionInput, ActionOutput]]]=None,
        postprocess: Optional[List[Action[ActionInput, ActionOutput]]]=None,
        input_class: Type[TextEmbeddingInput]=TextEmbeddingInput,
        output_class: Type[TextEmbeddingOutput]=TextEmbeddingOutput
    ) -> None:
        

        if not predictor:
            model = AutoModel.from_pretrained(self.default_model) # type: ignore
            predictor = TransformersModel(
                TransformersModelConfig(
                    model=model # type: ignore
                ),
                input_class=ModelInput,
                output_class=ModelOutput
            )

        super().__init__(
            predictor=predictor,
            preprocess=preprocess or [
                EmbeddingPreprocessor(
                    EmbeddingPreprocessorConfig(
                        tokenizer=AutoTokenizer.from_pretrained( # type: ignore 
                            self.default_model
                        )
                    )
                )
            ],
            postprocess=postprocess or [ # type: ignore
                EmbeddingPostprocessor(),
                ConvertEmbeddingsToNumpyArrays()    
            ],
            input_class=input_class, 
            output_class=output_class,
        )