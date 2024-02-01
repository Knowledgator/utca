from typing import Tuple, Any, Dict, Optional, Union

import spacy
from spacy.language import Language
from pydantic import PrivateAttr

from implementation.tasks.token_searcher.base_token_searcher_task.base_token_searcher import (
    InputWithThreshold, BaseTokenSearcher, BaseTokenSearcherConfig, BaseTokenSearcherOutput
)

class NERInput(InputWithThreshold):
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


class NEROutput(BaseTokenSearcherOutput):
    pass


class NERConfig(BaseTokenSearcherConfig):
    pass


class TokenSearcherNERTask(BaseTokenSearcher):
    prompt: str = """
Identify entities in the text having the following classes:
{label}
Text:
 {text}"""

    def __init__(self, cfg: NERConfig) -> None:
        super().__init__(cfg) 

        self.nlp: Language = spacy.load(
            'en_core_web_sm', 
            disable = ['lemmatizer', 'parser', 'tagger', 'ner']
        )
        self.nlp.add_pipe('sentencizer')
    

    def get_last_sentence_id(self, i: int, sentences_len: int) -> int:
        return min(i + self.cfg.sents_batch, sentences_len) - 1


    def chunkanize(self, text: str) -> Tuple[list[str], list[int]]:
        doc = self.nlp(text)
        chunks: list[str] = []
        starts: list[int] = []
        sentences = list(doc.sents)

        for i in range(0, len(sentences), self.cfg.sents_batch):
            start = sentences[i].start_char
            starts.append(start)

            last_sentence = self.get_last_sentence_id(i, len(sentences))
            end = sentences[last_sentence].end_char

            chunks.append(text[start:end])
        return chunks, starts
    

    def get_inputs(
        self, chunks: list[str], labels: list[str]
    ) -> Tuple[list[str], list[int]]:
        inputs: list[str] = []
        prompts_lens: list[int] = []

        for label in labels:
            prompt = self.prompt.format(label)
            prompts_lens.append(len(prompt))
            for chunk in chunks:
                inputs.append(prompt + chunk)

        return inputs, prompts_lens


    def _preprocess(
        self, input_data: Union[NERInput, Dict[str, Any]]
    ) -> NERInput:
        input_data = (
            input_data if isinstance(
                input_data, 
                NERInput
            ) else NERInput.parse_obj(input_data)
        )
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
        self, input_data: NERInput
    ) -> list[Dict[str, Any]]:
        outputs: list[Dict[str, Any]] = []

        for id, output in enumerate(self.pipeline(inputs)): # type: ignore
            label = labels[id//len(chunks_starts)]
            shift = chunks_starts[id%len(chunks_starts)] - prompts_lens[id//len(chunks_starts)]
            for ent in output:
                start = ent['start'] + shift + 1
                end = ent['end'] + shift
                start, end, span = self.clean_span(start, end, text[start:end])
                if not span:
                    continue
                
                if ent['score'] >= threshold:
                    outputs.append({
                        'span': span,
                        'start': start,
                        'end': end,
                        'entity': label
                    })
        return outputs


    def execute(
        self, input_data: NERInput
    ) -> NEROutput:
        threshold = self.choose_threshold(input_data)
        
        outputs = self.predict(
            input_data.text, 
            inputs, 
            input_data.labels, 
            chunks_starts, 
            prompts_lens, 
            threshold
        )
        return {"text": input_data.text, "entities": outputs}
    

    def execute(
        self, 
        input_data: Union[NERInput, Dict[str, Any]]
    ) -> NEROutput:
        input_data = self._preprocess(input_data)
        return self._postprocess(
            input_data,
            self._process(input_data)
        )