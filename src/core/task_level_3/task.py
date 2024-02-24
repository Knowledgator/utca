from typing import Generic, Dict, Any, cast, List

from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import (
    InputType, OutputType, ConfigType, Transformable
)
from core.executable_level_1.actions import Action
from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import PredictorConfigType, PredictorInputType, PredictorOutputType
from core.task_level_3.schema import (
    InputWithThresholdType, NERConfigType, NEROutputType
)

class Task(
    Executable[ConfigType, InputType, OutputType],
    Generic[
        ConfigType, InputType, OutputType,
        PredictorConfigType, PredictorInputType, PredictorOutputType
    ]
):
    def __init__(
        self, 
        cfg: ConfigType, 
        Predictor: Predictor[
            PredictorConfigType, 
            PredictorInputType, 
            PredictorOutputType
        ],
        preprocess: Action,
        postprocess: Action
    ) -> None:
        super().__init__(cfg)
        self.predictor = Predictor
        self._preprocess = preprocess
        self._postprocess = postprocess

    
    def invoke(
        self, input_data: InputType
    ) -> Dict[str, Any]:
        processed_input = cast(
            Dict[str, Any],
            self._preprocess.execute(input_data.model_dump())
        )
        predicts = cast(Dict[str, Any], self.predictor.execute(
            Transformable({"inputs": processed_input["inputs"]})
        ).extract())
        return cast(Dict[str, Any], self._postprocess.execute({
            "inputs": processed_input,
            "outputs": predicts["outputs"]
        }))
    

    def invoke_batch(
        self, input_data: List[InputType]
    ) -> list[Dict[str, Any]]:
        raise Exception("TODO!")


class NERTask(
    Task[
        NERConfigType, InputWithThresholdType, NEROutputType,
        PredictorConfigType, PredictorInputType, PredictorOutputType
    ]
):
    ...


    # def choose_threshold(self, input_data: InputWithThresholdType) -> float:
    #     return (
    #         input_data.threshold 
    #         if not input_data.threshold is None 
    #         else self.cfg.threshold
    #     )
    

    # def _preprocess(
    #     self, input_data: InputWithThresholdType
    # ) -> InputWithThresholdType:
    #     input_data.threshold = self.choose_threshold(input_data)
    #     return input_data