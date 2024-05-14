from utca.core import Transformable
from utca.implementation.predictors import (
    TokenSearcherPredictor
)

def test_tokensearcher():
    predictor = TokenSearcherPredictor()
    actual_ouput = predictor(Transformable({
        "inputs": [(
            "Identify organizations mentioned in the text:"
            " The National Aeronautics and Space Administration"
            " (NASA) is an independent agency of the U.S. federal"
            " government responsible for the civilian space program,"
            " as well as aeronautics and space research."
        )]
    })).extract()

    expected_ouput = {"entity_group": "ENT", "score": 0.793671, "word": "NationalAeronauticsandSpaceAdministration", "start": 49, "end": 95}
    assert (
        expected_ouput["word"] 
        == actual_ouput["output"][0][0]["word"]
    )