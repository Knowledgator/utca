from utca.core import RenameAttribute
from utca.implementation.tasks import ( 
    TokenSearcherNER,
    TokenSearcherRelationExtraction,
    TokenSearcherRelationExtractionPreprocessor,
    TokenSearcherRelationExtractionPostprocessor,
)

entities = [
    {
        'start': 0, 
        'end': 12, 
        'span': 'Paul Hammond',
        'score': 0.5170295238494873,
        'entity': 'scientist'
    }, {
        'start': 40,
        'end': 64, 
        'span': 'Johns Hopkins University',
        'score': 0.9068581461906433,
        'entity': 'university'
    }, {
        'start': 343, 
        'end': 367, 
        'span': 'University of California',
        'score': 0.7246244549751282, 
        'entity': 'university'
    }, {
        'start': 369,
        'end': 382, 
        'span': 'San Francisco',
        'score': 0.7688668370246887, 
        'entity': 'city'
    }, {
        'start': 132,
        'end': 144, 
        'span': 'Neuroscience',
        'score': 0.9707749485969543,
        'entity': 'journal'
    }
]

text = "Paul Hammond, a renowned neurologist at Johns Hopkins University, has recently published a paper in the prestigious journal \"Nature Neuroscience\". \nHis research focuses on a rare genetic mutation, found in less than 0.01% of the population, that appears to prevent the development of Alzheimer's disease. Collaborating with researchers at the University of California, San Francisco, the team is now working to understand the mechanism by which this mutation confers its protective effect. \nFunded by the National Institutes of Health, their research could potentially open new avenues for Alzheimer's treatment."

def test_simple_preprocessor():
    r = TokenSearcherRelationExtractionPreprocessor().run({
        "entities": entities,
        "relations": [
            {
                "relation": "published at"
            },{
                "relation": "worked at"
            }
        ],
        "text": text
    })
    assert len(r["source_entities"]) == 2*len(entities)
    assert len(r["inputs"]) == 2*len(entities)


p = (
    TokenSearcherNER() 
    | RenameAttribute("output", "entities")
    | TokenSearcherRelationExtraction()
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
            "pairs_filter": [("scientist", "university"), ("scientist", "other")]
        }]
    })
    assert r["output"][0]["target"]["span"] =="Johns Hopkins University"
    assert r["output"][1]["target"]["span"] == "University of California"


def test_pipeline_threshold():
    pt = (
        TokenSearcherNER() 
        | RenameAttribute("output", "entities")
        | TokenSearcherRelationExtraction(
            postprocess=TokenSearcherRelationExtractionPostprocessor(threshold=0.6)
        )
    )
    r = pt.run({
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
            "pairs_filter": [("scientist", "university"), ("scientist", "other")]
        }]
    })
    assert r["output"][0]["target"]["span"] == "University of California"


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
