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

    expected_ouput = {"label": "planet", "score": 0.9, "text": "Earth", "start": 0, "end": 5}
    assert (
        expected_ouput["text"] 
        == actual_ouput["output"][0][0]["text"]
    )