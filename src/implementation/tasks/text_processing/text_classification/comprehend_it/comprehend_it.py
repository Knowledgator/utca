from typing import Any, Dict, List, Optional, Union, Type

from core.executable_level_1.schema import (
    Input, 
    Output,
    Config 
)
from core.executable_level_1.actions import (
    OneToOne, OneToMany, ManyToOne, ManyToMany
)
from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import (
    PredictorConfig,
    PredictorInput,
    PredictorOutput
)
from core.task_level_3.task import Task
from implementation.predictors.comprehend_it.predictor import (
    ComprehendItPredictor
)

class ComprehendItInput(Input):
    text: str
    labels: List[str]


class ComprehendItOutput(Output):
    outputs: Dict[str, Any]


class ComprehendIt(
    Task[
        Config,
        ComprehendItInput,
        ComprehendItOutput
    ]
):
    def __init__(
        self,
        *,
        cfg: Optional[Config]=None, 
        predictor: Optional[Predictor[
            PredictorConfig, 
            PredictorInput, 
            PredictorOutput
        ]]=None,
        preprocess: Optional[List[Union[OneToOne, OneToMany, ManyToOne, ManyToMany]]]=None,
        postprocess: Optional[List[Union[OneToOne, OneToMany, ManyToOne, ManyToMany]]]=None,
        input_class: Type[ComprehendItInput]=ComprehendItInput,
        output_class: Type[ComprehendItOutput]=ComprehendItOutput
    ) -> None:
        if not predictor:
            predictor = ComprehendItPredictor()

        super().__init__(
            cfg=cfg, 
            predictor=predictor,
            preprocess=preprocess or [],
            postprocess=postprocess or [],
            input_class=input_class, 
            output_class=output_class,
        )

