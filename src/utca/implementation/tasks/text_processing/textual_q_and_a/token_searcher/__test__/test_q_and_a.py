from core.executable_level_1.schema import Transformable
from implementation.tasks.text_processing.textual_q_and_a.token_searcher.token_searcher import (
    TokenSearcherQandA
)

def test_tokensearcher_general():
    task = TokenSearcherQandA()
    res = task(Transformable({
        "question": "Who are the founders of Microsoft?",
        "text": "Microsoft was founded by Bill Gates and Paul Allen on April 4, 1975 to develop and sell BASIC interpreters for the Altair 8800. During his career at Microsoft, Gates held the positions of chairman, chief executive officer, president and chief software architect, while also being the largest individual shareholder until May 2014."
    })).extract()
    assert "Bill Gates and Paul Allen" == res["output"][0]["span"]