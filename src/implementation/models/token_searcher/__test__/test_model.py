from implementation.models.token_searcher.model import (
    TokenSearcherModel
)
from implementation.models.token_searcher.schema import (
    TokenSearcherModelConfig
)

def test_tokensearcher():
    cfg = TokenSearcherModelConfig(
        model='knowledgator/UTC-DeBERTa-small',
        device='cpu'
    )

    model = TokenSearcherModel(cfg)
    actual_ouput = model.execute({
        "inputs": [(
            "Identify organizations mentioned in the text:"
            " The National Aeronautics and Space Administration"
            " (NASA) is an independent agency of the U.S. federal"
            " government responsible for the civilian space program,"
            " as well as aeronautics and space research."
        )]
    })

    expected_ouput = {'entity_group': 'ENT', 'score': 0.793671, 'word': 'NationalAeronauticsandSpaceAdministration', 'start': 49, 'end': 95}
    assert (
        expected_ouput['word'] 
        == actual_ouput.output[0][0]['word']
    )