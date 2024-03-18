from typing import Any, Dict, Tuple, Optional, cast

from core.executable_level_1.schema import Config
from core.executable_level_1.actions import Action
from core.task_level_3.objects.objects import (
    ClassifiedEntity
)
from core.task_level_3.utils import (
    build_entity, sent_tokenizer
)

class TokenSearcherNERPreprocessorConfig(Config):
    sents_batch: int=10


class TokenSearcherNERPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    prompt: str = """
Identify entities in the text having the following classes:
{label}
Text:
 """
    def __init__(
        self, 
        cfg: Optional[TokenSearcherNERPreprocessorConfig]=None
    ) -> None:
        self.cfg = cfg or TokenSearcherNERPreprocessorConfig()

    
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


    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        input_data["chunks"], input_data["chunks_starts"] = (
            self.chunkanize(input_data["text"])
        )
        input_data["inputs"], input_data["prompts_lens"] = (
            self.get_inputs(
                input_data["chunks"], 
                input_data["labels"]
            )
        )
        return input_data


class TokenSearcherNERPostprocessorConfig(Config):
    threshold: float = 0.


class TokenSearcherNERPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    def __init__(
        self, 
        cfg: Optional[TokenSearcherNERPostprocessorConfig]=None
    ) -> None:
        self.cfg = cfg or TokenSearcherNERPostprocessorConfig()
    
    
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        outputs: list[ClassifiedEntity] = []

        for id, output in enumerate(input_data["output"]):
            label = cast(str,
                input_data["labels"]
                [id//len(input_data["chunks_starts"])]
            )
            shift = (
                input_data["chunks_starts"][id%len(input_data["chunks_starts"])] 
                - input_data["prompts_lens"][id//len(input_data["chunks_starts"])]
            )
            for ent in output:
                if entity := build_entity(
                    input_data["text"], 
                    ent, 
                    self.cfg.threshold, 
                    label, 
                    shift=shift
                ):
                    outputs.append(entity)
        return {
            "text": input_data["text"],
            "output": outputs
        }