from utca.core import RenameAttribute
from utca.implementation.predictors import (
    GLiNERPredictor,
    GLiNERPredictorConfig
)
from utca.implementation.tasks import (
    GLiNER,
    GLiNERRelationExtraction,
)

predictor = GLiNERPredictor(
    GLiNERPredictorConfig(
        model_name = "knowledgator/gliner-multitask-large-v0.5",
    )
)

p = (
    GLiNER( 
        predictor=predictor,
    ) 
    | RenameAttribute("output", "entities")
    | GLiNERRelationExtraction(
        predictor=predictor,
    )
)

def test_pipeline():
    r = p.run({
        "text": "Dr. Paul Hammond, a renowned neurologist at Johns Hopkins University, has recently published a paper in the prestigious journal \"Nature Neuroscience\". \nHis research focuses on a rare genetic mutation, found in less than 0.01% of the population, that appears to prevent the development of Alzheimer's disease. Collaborating with researchers at the University of California, San Francisco, the team is now working to understand the mechanism by which this mutation confers its protective effect. \nFunded by the National Institutes of Health, their research could potentially open new avenues for Alzheimer's treatment.",
        "labels": [
            "scientist",
            "university",
            "city",
            "journal",
        ],
        "relations": [{
            "relation": "published at",
            "pairs_filter": [("scientist", "journal")]
        },{
            "relation": "worked at",
            "pairs_filter": [("scientist", "university")]
        }]
    })
    assert r["output"][0]["target"]["span"] =="Johns Hopkins University"


def test_distance_threshold():
    r = p.run({
        "text": "Dr. Paul Hammond, a renowned neurologist at Johns Hopkins University, has recently published a paper in the prestigious journal \"Nature Neuroscience\". \nHis research focuses on a rare genetic mutation, found in less than 0.01% of the population, that appears to prevent the development of Alzheimer's disease. Collaborating with researchers at the University of California, San Francisco, the team is now working to understand the mechanism by which this mutation confers its protective effect. \nFunded by the National Institutes of Health, their research could potentially open new avenues for Alzheimer's treatment.",
        "labels": [
            "scientist",
        ],
        "relations": [{
            "relation": "worked at",
            "distance_threshold": 1
        }]
    })

    assert r["output"] == []
