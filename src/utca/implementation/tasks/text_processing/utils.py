from typing import Tuple, Iterator, cast

import nltk # type: ignore
nltk.download('punkt', quiet=True) # type: ignore
tokenizer = nltk.load("tokenizers/punkt/english.pickle") # type: ignore

def sent_tokenizer(text: str) -> Iterator[Tuple[int, int]]:
    return cast(Iterator[Tuple[int, int]], tokenizer.span_tokenize(text)) # type: ignore