from typing import Tuple, Any, Dict, Optional, cast, Type

from pydantic import PrivateAttr

from core.task_level_3.task import NERTask
from core.task_level_3.schema import (
    InputWithThreshold, 
    NEROutput,
    NERConfig 
)
from core.task_level_3.utils import (
    build_entity, sent_tokenizer
)
from core.task_level_3.objects.objects import (
    ClassifiedEntity
)
from implementation.models.token_searcher.schema import (
    TokenSearcherModelConfig, 
    TokenSearcherModelInput, 
    TokenSearcherModelOutput
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


class TokenSearcherNEROutput(NEROutput[ClassifiedEntity]):
    text: str


class TokenSearcherNERConfig(NERConfig):
    sents_batch: int=10


class TokenSearcherNERTask(
    NERTask[
        TokenSearcherNERConfig,
        TokenSearcherNERInput, 
        TokenSearcherNEROutput,
        TokenSearcherModelConfig, 
        TokenSearcherModelInput, 
        TokenSearcherModelOutput
    ]
):
    input_class: Type[TokenSearcherNERInput] = TokenSearcherNERInput
    output_class: Type[TokenSearcherNEROutput] = TokenSearcherNEROutput

    prompt: str = """
Identify entities in the text having the following classes:
{label}
Text:
 """
    
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
        self, input_data: TokenSearcherNERInput
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


    def invoke(
        self, input_data: TokenSearcherNERInput
    ) -> Dict[str, Any]:
        input_data = self._preprocess(input_data)
        predicts = self.model.execute(
            {'inputs': input_data.inputs}, Dict[str, Any]
        )
        return self._postprocess(
            input_data, predicts
        )
    

    def invoke_batch(
        self, input_data: list[TokenSearcherNERInput]
    ) -> list[Dict[str, Any]]:
        raise Exception('TODO!')


    def _postprocess(
        self, 
        input_data: TokenSearcherNERInput, 
        output_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        outputs: list[ClassifiedEntity] = []

        for id, output in enumerate(output_data['outputs']):
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
        return {
            'text': input_data.text,
            'output': outputs
        }