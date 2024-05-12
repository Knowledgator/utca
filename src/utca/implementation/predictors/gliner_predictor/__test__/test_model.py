from utca.core.executable_level_1.schema import Transformable
from utca.implementation.predictors.gliner_predictor.predictor import (
    GLiNERPredictor
)
from utca.implementation.predictors.gliner_predictor.schema import (
    GLiNERPredictorConfig
)
def test_gliner():
    config = GLiNERPredictorConfig()
    predictor = GLiNERPredictor(config)
    actual_ouput = predictor(Transformable({
        "texts": ["Earth is the most beautiful planet."],
        "labels": ["planet", "rocket", "star"],
        "threshold": 0.5,
    })).extract()

    expected_ouput = {"label": "planet", "score": 0.9, "text": "Earth", "start": 0, "end": 5}
    assert (
        expected_ouput["text"] 
        == actual_ouput["output"][0][0]["text"]
    )