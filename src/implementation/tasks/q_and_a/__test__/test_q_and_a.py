from implementation.tasks.q_and_a.token_searcher import (
    TokenSearcherQandATask
)

def test_tokensearcher_general():
    task = TokenSearcherQandATask()
    res = task.execute({
        "question": "Who are the founders of Microsoft?",
        "text": "Microsoft was founded by Bill Gates and Paul Allen on April 4, 1975 to develop and sell BASIC interpreters for the Altair 8800. During his career at Microsoft, Gates held the positions of chairman, chief executive officer, president and chief software architect, while also being the largest individual shareholder until May 2014."
    })

    assert "Bill Gates and Paul Allen" == res.output[0].span