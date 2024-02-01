import logging

from src.model_level_2.schema import Prompt
from implementation.models.token_searcher.model import (
    TokenSearcher, TokenSearcherConfigs
)

def test_tokensearcher():
    cfg = TokenSearcherConfigs(
        model_name='knowledgator/UTC-DeBERTa-small',
        device='cpu'
    )

    model = TokenSearcher(cfg)
    logging.error(model.invoke(Prompt("Identify organizations mentioned in the text: The National Aeronautics and Space Administration (NASA) is an independent agency of the U.S. federal government responsible for the civilian space program, as well as aeronautics and space research.")))

