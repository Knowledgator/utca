# from core.model_level_2.schema import BasicPrompt
from implementation.models.token_searcher.model import (
    # TokenSearcher, 
    TokenSearcherConfigs
)

from implementation.tasks.token_searcher.general.general_task import TokenSearcherGeneralTask

def test_tokensearcher_general():
    cfg = TokenSearcherConfigs(
        model_name='knowledgator/UTC-DeBERTa-small',
        device='cpu'
    )

    task = TokenSearcherGeneralTask('find_word', cfg)
    task.execute({'prompt': (
        "Identify organizations mentioned in the text:"
        " The National Aeronautics and Space Administration"
        " (NASA) is an independent agency of the U.S. federal"
        " government responsible for the civilian space program,"
        " as well as aeronautics and space research."
    )})