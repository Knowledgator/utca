from typing import (
    Any, Dict, List, Callable, Type, Optional, Union, cast
) 

from transformers import ( # type: ignore
    AutoConfig,
    AutoTokenizer,
    PreTrainedModel, 
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
    AutoModelForSeq2SeqLM,
    AutoModelForCausalLM,
)
import torch
import pyximport # type: ignore
pyximport.install() # type: ignore

from core.executable_level_1.actions import (
    Action, ActionInput, ActionOutput
)
from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import (
    PredictorInput,
    PredictorOutput
)
from core.task_level_3.task import Task
from core.task_level_3.schema import (
    Input, 
    Output,
)
from implementation.predictors.transformers.transformers_model import (
    TransformersGenerativeModel,
    TransformersModelConfig
)
from implementation.datasources.trie.labels_trie import LabelsTrie # type: ignore
from implementation.tasks.text_processing.entity_linking.transformers.actions import (
    EntityLinkingPreprocessing,
    EntityLinkingPostprocess
)

class EntityLinkingInput(Input):
    texts: List[str]
    num_beams: int
    num_return_sequences: int


class EntityLinkingOutput(Output):
    classification_output: Any


class ModelInput(PredictorInput):
    class Config:
        arbitrary_types_allowed = True

    encodings: Any
    num_beams: int
    num_return_sequences: int
    prefix_allowed_tokens_fn: Callable[
        [torch.Tensor, int], List[int]
    ]


class ModelOutput(PredictorOutput):
    class Config:
        arbitrary_types_allowed = True

    sequences: Any
    sequences_scores: Any


class EntityLinkingTask(
    Task[
        EntityLinkingInput, 
        EntityLinkingOutput,
    ]
):
    default_model = "openai-community/gpt2"


    def initialize_model(self, model: str) -> PreTrainedModel:
        """
        Model initialization

        Args:
            model (str): Model name or path.

        Raises:
            ValueError: If model doesnt exist or cant be found.

            ValueError: If provided model is not generative.
        
        Returns:
            PreTrainedModel: Initialized model.
        """        
        try:
            config = AutoConfig.from_pretrained(model) # type: ignore
        except Exception:
            raise ValueError(
                "The path to the model does't exist or it's unavailable on"
                " Hugging Face."
            )

        if config.is_encoder_decoder: # type: ignore
            return ( # type: ignore
                AutoModelForSeq2SeqLM # type: ignore
                .from_pretrained(model)
            )
        else:
            try:
                return ( # type: ignore
                    AutoModelForCausalLM # type: ignore
                    .from_pretrained(model)
                )
            except:
                raise ValueError("Expected generative model.")


    def initialize_labels_trie(self, labels: List[str]) -> None:
        """
        Initializing the labels trie

        Args:
            labels (List[str]): Labels that will be used.
        """ 
        tokenized_labels = []
        for label in labels:
            tokens = self.tokenizer.encode(label) # type: ignore
            if tokens[0] == self.tokenizer.bos_token_id:
                tokens = tokens[1:]
            tokenized_labels.append([self.pad_token_id] + tokens) # type: ignore
        self.trie: LabelsTrie = LabelsTrie(tokenized_labels)


    def _get_candidates(
        self, sent: torch.Tensor, prompt_len: int
    ) -> List[int]:
        """
        Get next possible candidates

        Args:
            sent (torch.Tensor): Tensor.
            prompt_len (int): Prompt length.

        Returns:
            List[int]: Possible next tokens.
        """        
        gen_sent: List[int] = sent.tolist() # type: ignore
        if not self.encoder_decoder:
            gen_sent = [self.pad_token_id, *gen_sent[prompt_len:]]

        return (
            self.trie.get(gen_sent) # type: ignore
            or [self.tokenizer.eos_token_id]
        )


    def __init__(
        self,
        *,
        labels: List[str],
        tokenizer: Optional[Union[
            str, PreTrainedTokenizer, PreTrainedTokenizerFast
        ]]=None,
        predictor: Optional[Predictor[
            PredictorInput, 
            PredictorOutput
        ]]=None,
        preprocess: Optional[List[Action[ActionInput, ActionOutput]]]=None,
        postprocess: Optional[List[Action[ActionInput, ActionOutput]]]=None,
        input_class: Type[EntityLinkingInput]=EntityLinkingInput,
        output_class: Type[EntityLinkingOutput]=EntityLinkingOutput
    ) -> None:
        if not tokenizer:
            self.tokenizer = AutoTokenizer.from_pretrained(self.default_model) # type: ignore
        elif isinstance(tokenizer, str):
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer) # type: ignore
        else:
            self.tokenizer = tokenizer

        self.tokenizer.padding_side = "left" # type: ignore

        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

        self.pad_token_id: int = cast(int, self.tokenizer.pad_token_id)

        if not predictor:
            model = self.initialize_model(self.default_model)
            predictor = TransformersGenerativeModel(
                TransformersModelConfig(
                    model=model, # type: ignore
                    kwargs={
                        "max_new_tokens": 512,
                        "pad_token_id": self.pad_token_id,
                        "return_dict_in_generate": True,
                        "output_scores": True, 
                    }
                ),
                input_class=ModelInput,
                output_class=ModelOutput
            )
        self.encoder_decoder: bool = predictor.config.is_encoder_decoder
        self.initialize_labels_trie(labels)

        super().__init__(
            predictor=predictor,
            preprocess=preprocess or [ # type: ignore
                EntityLinkingPreprocessing() 
            ],
            postprocess=postprocess or [ # type: ignore
                EntityLinkingPostprocess( 
                    tokenizer=self.tokenizer,
                    encoder_decoder=self.encoder_decoder
                )  
            ],
            input_class=input_class, 
            output_class=output_class,
        )


    def invoke(self, input_data: EntityLinkingInput) -> Dict[str, Any]:
        processed_input = self.process(
            input_data.generate_transformable(), 
            self._preprocess # type: ignore
        ) 
        tokenized_prompt = self.tokenizer( # type: ignore
            getattr(processed_input, "texts"), 
            return_tensors="pt",
            padding=True,
            truncation=True
        )
        prompt_len = tokenized_prompt["input_ids"].shape[-1] # type: ignore
        processed_input.prefix_allowed_tokens_fn = ( # type: ignore
            lambda _, sent: self._get_candidates(sent, prompt_len) # type: ignore
        )
        processed_input.encodings = tokenized_prompt # type: ignore
        predicts = self.predictor(processed_input)
        return self.process(
            predicts, 
            self._postprocess # type: ignore
        ).extract()  