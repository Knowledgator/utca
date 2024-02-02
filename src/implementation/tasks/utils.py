from typing import Tuple

import nltk # type: ignore

tokenizer = nltk.load("tokenizers/punkt/english.pickle") # type: ignore

def sent_tokenizer(text: str) -> list[Tuple[int, int]]:
    return tokenizer.span_tokenize(text) # type: ignore
    