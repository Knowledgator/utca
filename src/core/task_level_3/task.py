from typing import Type, Dict, Any, List, Union, Optional, Callable

from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import (
    Input, Output, InputType, OutputType, Transformable
)
from core.executable_level_1.actions import Action
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.schema import (
    InputWithThresholdType, NEROutputType
)

class Task(
    Executable[InputType, OutputType],
):
    def __init__(
        self,
        *,
        predictor: Predictor[Input, Output],
        preprocess: Optional[List[Action[Any, Any]]],
        postprocess: Optional[List[Action[Any, Any]]],
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
            Action[Any, Any],
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