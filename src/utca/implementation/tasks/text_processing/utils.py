from typing import Tuple, Iterator, cast

import nltk
from nltk.tokenize import PunktTokenizer

nltk.download('punkt_tab', quiet=True)
tokenizer = PunktTokenizer()

def sent_tokenizer(text: str) -> Iterator[Tuple[int, int]]:
    return cast(Iterator[Tuple[int, int]], tokenizer.span_tokenize(text)) # type: ignore