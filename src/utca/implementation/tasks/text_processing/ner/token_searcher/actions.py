from typing import Any, Dict, List, Optional, Tuple, cast

from utca.core.executable_level_1.actions import Action
from utca.core.task_level_3.objects.objects import (
    ClassifiedEntity
)
from utca.implementation.predictors.token_searcher.utils import (
    build_entity
)
from utca.implementation.tasks.text_processing.utils import sent_tokenizer

class TokenSearcherNERPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Create prompts with provided text

    Arguments:
        input_data (Dict[str, Any]): Expected keys:
            "text" (str): Text to process;

            "labels" (List[str]): Labels for classification;

    Returns:
        Dict[str, Any]: Expected keys:
            "inputs" (List[str]): Model inputs;

            "chunks_starts" (List[int]): Chunks start positions. Used by postprocessor;
            
            "prompt_lengths" (List[int]): Prompt lenghts. Used by postprocessor;
    """

    prompt: str = """
Identify entities in the text having the following classes:
{label}
Text:
"""
    def __init__(
        self, 
        sents_batch: int=10,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            sents_batch (int): Chunks size in sentences. Defaults to 10.

            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.sents_batch = sents_batch

    
    def get_last_sentence_id(self, i: int, sentences_len: int) -> int:
        return min(i + self.sents_batch, sentences_len) - 1


    def chunkanize(self, text: str) -> Tuple[List[str], List[int]]:
        chunks: List[str] = []
        starts: List[int] = []

        sentences: List[Tuple[int, int]] = list(sent_tokenizer(text))

        for i in range(0, len(sentences), self.sents_batch):
            start = sentences[i][0]
            starts.append(start)

            last_sentence = self.get_last_sentence_id(i, len(sentences))
            end = sentences[last_sentence][-1]

            chunks.append(text[start:end])
        return chunks, starts


    def get_inputs(
        self, chunks: List[str], labels: List[str]
    ) -> Tuple[List[str], List[int]]:
        inputs: List[str] = []
        prompts_lens: List[int] = []

        for label in labels:
            prompt = self.prompt.format(label=label)
            prompts_lens.append(len(prompt))
            for chunk in chunks:
                inputs.append(prompt + chunk)

        return inputs, prompts_lens


    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Arguments:
            input_data (Dict[str, Any]): Expected keys:
                "text" (str): Text to process;

                "labels" (List[str]): Labels for classification;

        Returns:
            Dict[str, Any]: Expected keys:
                "inputs" (List[str]): Model inputs;

                "chunks_starts" (List[int]): Chunks start positions. Used by postprocessor;
                
                "prompt_lengths" (List[int]): Prompt lenghts. Used by postprocessor;
        """
        chunks, chunks_starts = (
            self.chunkanize(input_data["text"])
        )
        inputs, prompts_lengths = (
            self.get_inputs(
                chunks,
                input_data["labels"]
            )
        )
        return {
            "inputs": inputs,
            "chunks_starts": chunks_starts,
            "prompts_lengths": prompts_lengths,
        }


class TokenSearcherNERPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Format output

    Arguments:
        input_data (Dict[str, Any]): Expected keys:
            "output" (List[List[Dict[str, Any]]]): Model output;

            "labels" (List[str]): Labels for classification;
            
            "text" (str): Processed text;
            
            "chunks_starts" (List[int]): Chunks start positions;
            
            "prompt_lengths" (List[int]): Prompt lenghts;
            
    Returns:
        Dict[str, Any]: Expected keys:
            "text" (str): Processed text;
            
            "output" (List[ClassifiedEntity]): Classified entities;
    """
    def __init__(
        self, 
        threshold: float=0.,
        name: Optional[str]=None,
    ) -> None:
        """
        Arguments:
            threshold (float): Entities threshold score. Defaults to 0.
            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.      
        """
        super().__init__(name)
        self.threshold = threshold
    
    
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Arguments:
            input_data (Dict[str, Any]): Expected keys:
                "output" (List[List[Dict[str, Any]]]): Model output;

                "labels" (List[str]): Labels for classification;
                
                "text" (str): Processed text;
                
                "chunks_starts" (List[int]): Chunks start positions;
                
                "prompt_lengths" (List[int]): Prompt lenghts;

        Returns:
            Dict[str, Any]: Expected keys:
                "text" (str): Processed text;
                
                "output" (List[ClassifiedEntity]): Classified entities;
        """
        outputs: List[ClassifiedEntity] = []

        for id, output in enumerate(input_data["output"]):
            label = cast(str,
                input_data["labels"]
                [id//len(input_data["chunks_starts"])]
            )
            shift = (
                input_data["chunks_starts"][id%len(input_data["chunks_starts"])] 
                - input_data["prompts_lengths"][id//len(input_data["chunks_starts"])]
            )
            for ent in output:
                if entity := build_entity(
                    input_data["text"], 
                    ent, 
                    self.threshold, 
                    label, 
                    shift=shift
                ):
                    outputs.append(entity)
        return {
            "text": input_data["text"],
            "output": outputs
        }