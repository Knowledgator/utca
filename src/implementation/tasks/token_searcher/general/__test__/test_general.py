from implementation.models.token_searcher.model import (
    TokenSearcherModel, TokenSearcherModelConfig
)
from implementation.tasks.token_searcher.general.task import (
    TokenSearcherGeneralTask, TokenSearcherGeneralConfig
)

def test_tokensearcher_general():
    cfg = TokenSearcherGeneralConfig()

    task = TokenSearcherGeneralTask(
        cfg, TokenSearcherModel(TokenSearcherModelConfig(
            model="knowledgator/UTC-DeBERTa-small",
            device="cpu"
        ))
    )
    res = task.execute({"prompt": (
        "Identify organizations mentioned in the text:"
        " The National Aeronautics and Space Administration"
        " (NASA) is an independent agency of the U.S. federal"
        " government responsible for the civilian space program,"
        " as well as aeronautics and space research."
    )})

    assert "National Aeronautics and Space Administration" == res.output[0].span