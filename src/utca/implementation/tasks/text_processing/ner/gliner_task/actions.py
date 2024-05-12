from typing import Any, Dict, List, Optional, Tuple, cast

from utca.core.executable_level_1.actions import Action
from utca.core.task_level_3.objects.objects import (
    ClassifiedEntity
)
from utca.implementation.predictors.token_searcher.utils import sent_tokenizer

class GLiNERPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Create prompts with providied text

    Arguments:
        input_data (Dict[str, Any]): Expected keys:
            "text" (str): Text to process;

    Returns:
        Dict[str, Any]: Expected keys:
            "inputs" (List[str]): Model inputs;

            "chunks_starts" (List[int]): Chunks start positions. Used by postprocessor;
            
            "prompt_lengths" (List[int]): Prompt lenghts. Used by postprocessor;
    """

    def __init__(
        self, 
        sents_batch: int=10,
        threshold: float=0.5,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            labels (List[str]) - list of labels to recognize in a text.

            sents_batch (int): Chunks size in sentences. Defaults to 10.

            threshold (float): Minimial score to put entities into the output.

            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.threshold = threshold
        self.sents_batch = sents_batch

    
    def get_last_sentence_id(self, i: int, sentences_len: int) -> int:
        return min(i + self.sents_batch, sentences_len) - 1


    def chunkanize(self, text: str) -> Tuple[List[str], List[int]]:
        chunks: List[str] = []
        starts: List[int] = []

        sentences: List[Tuple[int, int]] = [*sent_tokenizer(text)]

        for i in range(0, len(sentences), self.sents_batch):
            start = sentences[i][0]
            starts.append(start)

            last_sentence = self.get_last_sentence_id(i, len(sentences))
            end = sentences[last_sentence][0]

            chunks.append(text[start:end])
        return chunks, starts

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
                "texts" (List[str]): Model inputs;

                "chunks_starts" (List[int]): Chunks start positions. Used by postprocessor;
                
                "threshold" (float): Minimal score for an entity to put into output;
        """
        chunks, chunks_starts = (
            self.chunkanize(input_data["text"])
        )
        return {
            "texts": chunks,
            "chunks_starts": chunks_starts,
            "threshold": self.threshold,
        }


class GLiNERPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Format output

    Arguments:
        input_data (Dict[str, Any]): Expected keys:
            "output" (List[List[Dict[str, Any]]]): Model output;

            "labels" (List[str]): Labels for classification;
            
            "text" (str): Processed text;
            
            "chunks_starts" (List[int]): Chunks start positions;
            
            
    Returns:
        Dict[str, Any]: Expected keys:
            "text" (str): Processed text;
            
            "output" (List[ClassifiedEntity]): Classified entities;
    """
    def __init__(
        self, 
        name: Optional[str]=None,
    ) -> None:
        """
        Arguments:            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.      
        """
        super().__init__(name)
    
    
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
                
        Returns:
            Dict[str, Any]: Expected keys:
                "text" (str): Processed text;
                
                "output" (List[ClassifiedEntity]): Classified entities;
        """
        outputs: List[ClassifiedEntity] = []

        for id, output in enumerate(input_data["output"]):
            shift = input_data["chunks_starts"][id]
            for ent in output:
                start = ent['start'] + shift
                end = ent['end'] + shift
                cls_ent = ClassifiedEntity(
                    start=start,
                    end=end,
                    span=ent['text'],
                    score=ent['score'],
                    entity=ent['label']
                )
                outputs.append(cls_ent)
        return {
            "text": input_data["text"],
            "output": outputs
        }