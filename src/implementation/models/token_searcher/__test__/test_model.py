from core.model_level_2.schema import BasicPrompt
from implementation.models.token_searcher.model import (
    TokenSearcher, TokenSearcherConfigs
)

def test_tokensearcher():
    cfg = TokenSearcherConfigs(
        model_name='knowledgator/UTC-DeBERTa-small',
        device='cpu'
    )

    model = TokenSearcher(cfg)
    actual_ouput = model.invoke(BasicPrompt(prompt=(
        "Identify organizations mentioned in the text:"
        " The National Aeronautics and Space Administration"
        " (NASA) is an independent agency of the U.S. federal"
        " government responsible for the civilian space program,"
        " as well as aeronautics and space research."
    )))
    expected_ouput = {'outputs': [[{'entity_group': 'ENT', 'score': 0.793671, 'word': 'NationalAeronauticsandSpaceAdministration', 'start': 49, 'end': 95}]]}
    assert (
        expected_ouput['outputs'][0][0]['word'] 
        == actual_ouput['outputs'][0][0]['word']
    )