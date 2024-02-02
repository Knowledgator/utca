from typing import Tuple, Any, Dict, Optional, Union, cast, Type

from pydantic import PrivateAttr

from implementation.tasks.utils import sent_tokenizer
from implementation.tasks.token_searcher.base_token_searcher_task.base_token_searcher import (
    BaseTokenSearcher
)
from implementation.tasks.token_searcher.base_token_searcher_task.schema import (
    InputWithThreshold, 
    BaseTokenSearcherOutput, 
    BaseTokenSearcherConfig
)
from implementation.tasks.token_searcher.base_token_searcher_task.utils import (
    build_entity
)
from implementation.models.token_searcher.objects import (
    ClassifiedEntity
)

class TokenSearcherNERInput(InputWithThreshold):
    text: str
    labels: list[str]
    _prompts: Optional[list[str]] = PrivateAttr()
    _prompt_lens: Optional[list[int]] = PrivateAttr()
    _chunks: Optional[list[str]] = PrivateAttr()
    _chunk_starts: Optional[list[int]] = PrivateAttr()

    def set_inputs(
        self,
        prompts: list[str], 
        prompts_lens: list[int],
        chunks: list[str],
        chunk_starts: list[int]
    ) -> None:
        self._prompts = prompts
        self._prompt_lens = prompts_lens
        self._chunks = chunks
        self._chunk_starts = chunk_starts

    
    @property
    def inputs(self) -> list[str]:
        return cast(list[str], self._prompts)
    

    @property
    def chunk_starts(self) -> list[int]:
        return cast(list[int], self._chunk_starts)
    

    @property
    def prompt_lens(self) -> list[int]:
        return cast(list[int], self._prompt_lens)


class TokenSearcherNEROutput(BaseTokenSearcherOutput[ClassifiedEntity]):
    text: str


class TokenSearcherNERConfig(BaseTokenSearcherConfig):
    ...


class TokenSearcherNERTask(
    BaseTokenSearcher[
        TokenSearcherNERConfig,
        TokenSearcherNERInput, 
        TokenSearcherNEROutput
    ]
):
    input_data_type: Type[TokenSearcherNERInput] = TokenSearcherNERInput
    prompt: str = """
Identify entities in the text having the following classes:
{label}
Text:
 """

    def __init__(self, cfg: TokenSearcherNERConfig) -> None:
        super().__init__(cfg)
    

    def get_last_sentence_id(self, i: int, sentences_len: int) -> int:
        return min(i + self.cfg.sents_batch, sentences_len) - 1


    def chunkanize(self, text: str) -> Tuple[list[str], list[int]]:
        chunks: list[str] = []
        starts: list[int] = []

        sentences: list[Tuple[int, int]] = [*sent_tokenizer(text)]

        for i in range(0, len(sentences), self.cfg.sents_batch):
            start = sentences[i][0]
            starts.append(start)

            last_sentence = self.get_last_sentence_id(i, len(sentences))
            end = sentences[last_sentence][0]

            chunks.append(text[start:end])
        return chunks, starts
    

    def get_inputs(
        self, chunks: list[str], labels: list[str]
    ) -> Tuple[list[str], list[int]]:
        inputs: list[str] = []
        prompts_lens: list[int] = []

        for label in labels:
            prompt = self.prompt.format(label=label)
            prompts_lens.append(len(prompt))
            for chunk in chunks:
                inputs.append(prompt + chunk)

        return inputs, prompts_lens


    def _preprocess(
        self, input_data: Union[TokenSearcherNERInput, Dict[str, Any]]
    ) -> TokenSearcherNERInput:
        input_data = super()._preprocess(input_data)
        chunks, chunks_starts = self.chunkanize(input_data.text)
        prompts, prompts_lens = self.get_inputs(chunks, input_data.labels)

        input_data.set_inputs(
            prompts=prompts,
            prompts_lens=prompts_lens,
            chunks=chunks, 
            chunk_starts=chunks_starts
        )
        return input_data


    def _process(
        self, input_data: TokenSearcherNERInput
    ) -> list[list[Dict[str, Any]]]:
        return self.get_predictions(input_data.inputs)
    

    def _postprocess(
        self, 
        input_data: TokenSearcherNERInput, 
        predicts: list[list[Dict[str, Any]]]
    ) -> TokenSearcherNEROutput:
        outputs: list[ClassifiedEntity] = []

        for id, output in enumerate(predicts): # type: ignore
            label = input_data.labels[id//len(input_data.chunk_starts)]
            shift = (
                input_data.chunk_starts[id%len(input_data.chunk_starts)] 
                - input_data.prompt_lens[id//len(input_data.chunk_starts)]
            )
            for ent in output:
                if entity := build_entity(
                    input_data.text, ent, cast(float, input_data.threshold), label, shift=shift
                ):
                    outputs.append(entity)
        return TokenSearcherNEROutput(
            text=input_data.text,
            output=outputs
        )