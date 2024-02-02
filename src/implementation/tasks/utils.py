from typing import Tuple, Iterator

import nltk # type: ignore

tokenizer = nltk.load("tokenizers/punkt/english.pickle") # type: ignore

def sent_tokenizer(text: str) -> Iterator[Tuple[int, int]]:
    return tokenizer.span_tokenize(text) # type: ignore
    