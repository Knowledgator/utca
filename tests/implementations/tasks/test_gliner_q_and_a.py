from utca.implementation.tasks import (
    GLiNERQandA
)

def test_default():
    text = "Microsoft was founded by Bill Gates and Paul Allen on April 4, 1975, to develop and sell BASIC interpreters for the Altair 8800. During his career at Microsoft, Gates held the positions of chairman, chief executive officer, president and chief software architect, while also being the largest individual shareholder until May 2014."
    pipe = GLiNERQandA()
    answer = pipe.run({
        "text": text,
        "question": "Who was the CEO of Microsoft?"
    })["output"][0]
    assert answer["span"] == text[answer["start"]:answer["end"]]