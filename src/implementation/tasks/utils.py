from typing import Iterator, Tuple

import nltk # type: ignore

tokenizer = nltk.load("tokenizers/punkt/english.pickle") # type: ignore

def sent_tokenizer(text: str) -> Iterator[Tuple[int, int]]:
    for start, end in tokenizer.span_tokenize(text): # type: ignore
        yield start, end
    