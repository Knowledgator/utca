from typing import Any, Dict, List, Generator, Optional, Tuple

from utca.core.executable_level_1.actions import Action
from utca.core.task_level_3.objects.objects import (
    Entity
)
from utca.implementation.tasks.text_processing.utils import sent_tokenizer

class GLiNERQandAPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Preprocess inputs

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "text" (str): Text to process;

            "question" (str): Question to answer;

        Returns:
            Dict[str, Any]: Expected keys:
                "texts" (List[str]): Model inputs;

                "labels" (List[str]): Labels model inputs;

                "chunks_starts" (List[int]): Chunks start positions. Used by postprocessor;
                
                "threshold" (float): Minimal score for an entity to put into output;
    """
    def __init__(
        self, 
        sents_batch: int=10,
        threshold: float=0.5,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
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

        sentences: List[Tuple[int, int]] = list(sent_tokenizer(text))

        for i in range(0, len(sentences), self.sents_batch):
            start = sentences[i][0]
            starts.append(start)

            last_sentence = self.get_last_sentence_id(i, len(sentences))
            end = sentences[last_sentence][-1]

            chunks.append(text[start:end])
        return chunks, starts
    

    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "text" (str): Text to process;

                "question" (str): Question to answer;

        Returns:
            Dict[str, Any]: Expected keys:
                "texts" (List[str]): Model inputs;

                "labels" (List[str]): Labels model inputs;

                "chunks_starts" (List[int]): Chunks start positions. Used by postprocessor;
                
                "threshold" (float): Minimal score for an entity to put into output;
        """
        chunks, chunks_starts = (
            self.chunkanize(input_data["text"])
        )
        return {
            "texts": [f'{input_data["question"]} {c}' for c in chunks],
            "labels": ["answer"],
            "chunks_starts": chunks_starts,
            "threshold": self.threshold,
        }
    

class GLiNERQandAPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Format output

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "output" (List[List[Dict[str, Any]]]): Model output;

            "chunks_starts" (List[int]): Chunks starts;

            "text" (str): Processed text;

            "question" (str): Answered question.

    Returns:
        Dict[str, Any]: Expected keys:
            "text" (str): Processed text;

            "question" (str): Answered question.
            
            "output" (List[Entity]): Answers;
    """
    def process_entities(
        self, 
        raw_entities: List[List[Dict[str, Any]]],
        chunks_starts: List[int],
        question_length: int,
    ) -> Generator[Entity, None, None]:
        for id, output in enumerate(raw_entities):
            shift = chunks_starts[id] - question_length - 1
            for ent in output:
                start = ent['start'] + shift
                end = ent['end'] + shift
                yield Entity(
                    start=start,
                    end=end,
                    span=ent['text'],
                    score=ent['score'],
                )

    
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "output" (List[List[Dict[str, Any]]]): Model output;

                "chunks_starts" (List[int]): Chunks starts;

                "text" (str): Processed text;

                "question" (str): Answered question.

        Returns:
            Dict[str, Any]: Expected keys:
                "text" (str): Processed text;

                "question" (str): Answered question.
                
                "output" (List[Entity]): Answers;
        """
        return {
            'text': input_data["text"],
            'question': input_data["question"],
            'output': list(self.process_entities(
                input_data["output"],
                input_data["chunks_starts"],
                len(input_data["question"])
            ))
        }