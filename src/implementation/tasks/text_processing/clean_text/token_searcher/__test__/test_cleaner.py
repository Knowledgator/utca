from typing import Dict, Any, cast

from core.executable_level_1.schema import Transformable
from implementation.tasks.text_processing.clean_text.token_searcher.token_searcher import (
    TokenSearcherTextCleanerTask
)
from implementation.tasks.text_processing.clean_text.token_searcher.actions import (
    TokenSearcherTextCleanerPostprocessor,
    TokenSearcherTextCleanerPostprocessorConfig
)

def test_tokensearcher_cleaner():
    task = TokenSearcherTextCleanerTask(
        postprocess=[TokenSearcherTextCleanerPostprocessor(
            TokenSearcherTextCleanerPostprocessorConfig(
                clean=True
            )
        )]
    )
    
    text = "The mechanism of action was characterized using native mass spectrometry, the thermal shift-binding assay, and enzymatic kinetic studies (Figure ). In the native mass spectrometry binding assay, compound 23R showed dose-dependent binding to SARS-CoV-2 Mpro, similar to the positive control GC376, with a binding stoichiometry of one drug per monomer (Figure A). Similarly, compound 23R showed dose-dependent stabilization of the SARS-CoV-2 Mpro in the thermal shift binding assay with an apparent Kd value of 9.43 μM, a 9.3-fold decrease compared to ML188 (1) (Figure B). In the enzymatic kinetic studies, 23R was shown to be a noncovalent inhibitor with a Ki value of 0.07 μM (Figure C, D top and middle panels). In comparison, the Ki for the parent compound ML188 (1) is 2.29 μM. The Lineweaver–Burk or double-reciprocal plot with different compound concentrations yielded an intercept at the Y-axis, suggesting that 23R is a competitive inhibitor similar to ML188 (1) (Figure C, D bottom panel). Buy our T-shirts for the lowerst prices you can find!!!  Overall, the enzymatic kinetic studies confirmed that compound 23R is a noncovalent inhibitor of SARS-CoV-2 Mpro."
    res = cast(Dict[str, Any], task.execute(Transformable({
        "text": text,
    })).extract())

    assert res["cleaned_text"]
    assert len(text) > len(res["cleaned_text"])