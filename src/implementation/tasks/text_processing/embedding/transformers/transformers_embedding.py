from typing import Dict, Type, Optional, List, Union, Any

from transformers import AutoModel, AutoTokenizer # type: ignore

from core.executable_level_1.actions import (
    OneToOne, OneToMany, ManyToOne, ManyToMany
)
from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import (
    PredictorConfig, PredictorInput, PredictorOutput
)
from core.predictor_level_2.schema import (
    PredictorConfig,
    PredictorInput,
    PredictorOutput
)
from core.task_level_3.task import Task
from core.task_level_3.schema import (
    Input, 
    Output,
    Config 
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


class TextEmbeddingTask(
    Task[
        Config,
        TextEmbeddingInput, 
        TextEmbeddingOutput,
    ]
):
    default_model = "BAAI/bge-large-en-v1.5"
    
    def __init__(
        self,
        *,
        cfg: Optional[Config]=None, 
        predictor: Optional[Predictor[
            PredictorConfig, 
            PredictorInput, 
            PredictorOutput
        ]]=None,
        preprocess: Optional[List[Union[OneToOne, OneToMany, ManyToOne, ManyToMany]]]=None,
        postprocess: Optional[List[Union[OneToOne, OneToMany, ManyToOne, ManyToMany]]]=None,
        input_class: Type[TextEmbeddingInput]=TextEmbeddingInput,
        output_class: Type[TextEmbeddingOutput]=TextEmbeddingOutput
    ) -> None:
        

        if not predictor:
            model = AutoModel.from_pretrained(self.default_model) # type: ignore
            predictor = TransformersModel(
                TransformersModelConfig(
                    model=model
                ),
                input_class=ModelInput
            )

        super().__init__(
            cfg=cfg, 
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
            postprocess=postprocess or [
                EmbeddingPostprocessor(),
                ConvertEmbeddingsToNumpyArrays()    
            ],
            input_class=input_class, 
            output_class=output_class,
        )

    
    def invoke(self, input_data: TextEmbeddingInput) -> Dict[str, Any]:
        return super().invoke(input_data)