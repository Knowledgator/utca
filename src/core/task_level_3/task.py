from typing import (
    Any, List, Dict, Type, Optional
)

from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.executable import Executable
from core.executable_level_1.schema import (
    Input, Output, Transformable
)
from core.executable_level_1.actions import Action
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.schema import NEROutputType

class Task(
    Executable[Input, Output]
):
    def __init__(
        self,
        *,
        predictor: Predictor[Any, Any],
        preprocess: Optional[List[Action[Any, Any]]],
        postprocess: Optional[List[Action[Any, Any]]],
        input_class: Type[Input],
        output_class: Type[Output],
        name: Optional[str]=None,
    ) -> None:
        super().__init__(
            input_class=input_class, 
            output_class=output_class, 
            name=name,
        )
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
        self, input_data: Input, evaluator: Evaluator
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
        Input, NEROutputType,
    ]
):
    ...