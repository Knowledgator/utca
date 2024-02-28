from typing import Type, Dict, Any, cast, List, Union, Optional

from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import (
    InputType, OutputType, ConfigType, Transformable
)
from core.executable_level_1.actions import (
    InputState, OutputState
)
from core.executable_level_1.actions import Action
from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import (
    PredictorConfigType, PredictorInputType, PredictorOutputType
)
from core.task_level_3.schema import (
    InputWithThresholdType, NERConfigType, NEROutputType
)

class Task(
    Executable[ConfigType, InputType, OutputType],
):
    def __init__(
        self,
        *,
        cfg: Optional[ConfigType]=None, 
        predictor: Predictor[
            PredictorConfigType, 
            PredictorInputType, 
            PredictorOutputType
        ],
        preprocess: List[Action[InputState, OutputState]],
        postprocess: List[Action[InputState, OutputState]],
        input_class: Type[InputType],
        output_class: Type[OutputType]
    ) -> None:
        super().__init__(cfg, input_class, output_class)
        self.predictor = predictor
        self._preprocess = preprocess
        self._postprocess = postprocess

    
    def process(
        self, state: InputState, actions: List[Action[InputState, OutputState]]
    ) -> Dict[str, Any]:
        tmp: Union[InputState, OutputState] = state
        for action in actions:
            tmp = action.execute(cast(InputState, tmp))
        return cast(Dict[str, Any], tmp)


    def invoke(
        self, input_data: InputType
    ) -> Dict[str, Any]:
        processed_input = cast(
            Dict[str, Any],
            self.process(input_data.model_dump(), self._preprocess)
        )
        predicts = cast(Dict[str, Any], self.predictor.execute(
            Transformable(processed_input)
        ).extract())
        return self.process(
            {
                "inputs": processed_input,
                "outputs": predicts["outputs"]
            }, 
            self._postprocess
        )
    

    def invoke_batch(
        self, input_data: List[InputType]
    ) -> List[Dict[str, Any]]:
        return [
            self.invoke(i) for i in input_data
        ]


class NERTask(
    Task[
        NERConfigType, InputWithThresholdType, NEROutputType,
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