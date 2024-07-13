from utca.implementation.predictors import (
    GLiNERPredictor
)
from utca.implementation.predictors import (
    GLiNERPredictorConfig
)

def test_gliner():
    config = GLiNERPredictorConfig()
    predictor = GLiNERPredictor(config)
    actual_ouput = predictor.run({
        "texts": ["Earth is the most beautiful planet."],
        "labels": ["planet", "rocket", "star"],
        "threshold": 0.5,
    })

    actual_ouput["output"][0][0]["score"] = 0.9
    expected_ouput = {"label": "planet", "score": 0.9, "text": "Earth", "start": 0, "end": 5}
    assert (
        expected_ouput
        == actual_ouput["output"][0][0]
    )


def test_gliner_repeated_or_empty_labels():
    predictor = GLiNERPredictor()
    actual_ouput = predictor.run({
        "texts": ["Earth is the most beautiful planet."],
        "labels": ["planet", "planet", "planet", "rocket", "star"],
        "threshold": 0.5,
    })
    
    actual_ouput["output"][0][0]["score"] = 0.9
    expected_ouput = {"label": "planet", "score": 0.9, "text": "Earth", "start": 0, "end": 5}
    assert (
        expected_ouput
        == actual_ouput["output"][0][0]
    )

    empty_res = predictor.run({
        "texts": ["Earth is the most beautiful planet."],
        "labels": [],
        "threshold": 0.5,
    })

    assert empty_res["output"] == [[]]

    empty_res = predictor.run({
        "texts": ["Earth is the most beautiful planet.", "And another one"],
        "labels": [],
        "threshold": 0.5,
    })

    assert empty_res["output"] == [[], []]