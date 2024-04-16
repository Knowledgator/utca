import pathlib
PATH = pathlib.Path(__file__).parent.resolve()

from implementation.datasources.pdf.actions import (
    PDFRead,
    PDFWrite,
    PDFExtractTexts
)

def test_pdf():
    PDFWrite().execute({
        "path_to_file": f"{PATH}/test.pdf",
        "text": "In the last few years, the number of programmers concerned about writing structured commit messages have dramatically grown. As exposed by Tim Pope in article readable commit messages are easy to follow when looking through the project history. Moreover the AngularJS contributing guides introduced conventions that can be used by automation tools to automatically generate useful documentation, or by developers during debugging process.\n\nThis document borrows some concepts, conventions and even text mainly from these two sources, extending them in order to provide a sensible guideline for writing commit messages.",
        "y_pending": 1
    })

    pdf = PDFRead().execute({
        "path_to_file": f"{PATH}/test.pdf"
    })

    assert PDFExtractTexts().execute(pdf)[1]