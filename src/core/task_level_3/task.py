from typing import Type, Dict, Any, List, Union, Optional, Callable

from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import (
    InputType, OutputType, Transformable
)
from core.executable_level_1.actions import (
    Action, ActionInput, ActionOutput
)
from core.predictor_level_2.predictor import Predictor
from core.predictor_level_2.schema import (
    PredictorInput, PredictorOutput
)
from core.task_level_3.schema import (
    InputWithThresholdType, NEROutputType
)

class Task(
    Executable[InputType, OutputType],
):
    def __init__(
        self,
        *,
        predictor: Predictor[
            PredictorInput, 
            PredictorOutput
        ],
        preprocess: Optional[List[Action[ActionInput, ActionOutput]]],
        postprocess: Optional[List[Action[ActionInput, ActionOutput]]],
        input_class: Type[InputType],
        output_class: Type[OutputType]
    ) -> None:
        super().__init__(input_class, output_class)
        self.predictor = predictor
        self._preprocess = preprocess
        self._postprocess = postprocess

    
    def process(
        self, 
        state: Transformable, 
        actions: List[Union[
            Action[ActionInput, ActionOutput],
            Callable[[Transformable], Transformable]
        ]]
    ) -> Transformable:
        for action in actions:
            state = action(state)
        return state


    def invoke(
        self, input_data: InputType
    ) -> Dict[str, Any]:
        processed_input = self.process(
            input_data.generate_transformable(), 
            self._preprocess # type: ignore
        )
        predicts = self.predictor(processed_input)
        return self.process(
            predicts,
            self._postprocess # type: ignore
        ).extract()


class NERTask(
    Task[
        InputWithThresholdType, NEROutputType,
    ]
):
    ...