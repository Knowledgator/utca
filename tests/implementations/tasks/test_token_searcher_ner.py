from utca.implementation.tasks.text_processing.ner.token_searcher.token_searcher import (
    TokenSearcherNER
)

def test_ner():
    task = TokenSearcherNER()
    res = task.run({
        "text": "Dr. Paul Hammond, a renowned neurologist at Johns Hopkins University, has recently published a paper in the prestigious journal \"Nature Neuroscience\". \nHis research focuses on a rare genetic mutation, found in less than 0.01% of the population, that appears to prevent the development of Alzheimer's disease. Collaborating with researchers at the University of California, San Francisco, the team is now working to understand the mechanism by which this mutation confers its protective effect. \nFunded by the National Institutes of Health, their research could potentially open new avenues for Alzheimer's treatment.",
        "labels": [
            "scientist",
            "university",
            "city"
        ],
    })
    assert len(res["output"]) == 4
    assert res["output"][0]["span"] == "Paul Hammond"