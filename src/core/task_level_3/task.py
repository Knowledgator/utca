from typing import (
    Any, List, Dict, Type, Optional
)

from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import (
    InputType, OutputType, Transformable
)
from core.executable_level_1.actions import Action
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.schema import NEROutputType

class Task(
    Executable[InputType, OutputType]
):
    def __init__(
        self,
        *,
        predictor: Predictor[Any, Any],
        preprocess: Optional[List[Action[Any, Any]]],
        postprocess: Optional[List[Action[Any, Any]]],
        input_class: Type[InputType],
        output_class: Type[OutputType]
    ) -> None:
        super().__init__(input_class, output_class)
        self.predictor = predictor
        self._preprocess = preprocess or []
        self._postprocess = postprocess or []

    
    def process(
        self, 
        state: Transformable, 
        actions: List[Action[Any, Any]],
        evaluator: Evaluator
    ) -> Transformable:
        for action in actions:
            state = action(state, evaluator)
        return state


    def invoke(
        self, input_data: InputType, evaluator: Evaluator
    ) -> Dict[str, Any]:
        processed_input = self.process(
            input_data.generate_transformable(), 
            self._preprocess,
            evaluator
        )
        predicts = self.predictor(processed_input, evaluator)
        return self.process(
            predicts,
            self._postprocess,
            evaluator
        ).extract()


class NERTask(
    Task[
        InputType, NEROutputType,
    ]
):
    ...