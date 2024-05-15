from typing import (
    Any, Dict, Type, Optional
)

from utca.core.executable_level_1.component import Component
from utca.core.executable_level_1.interpreter import Evaluator
from utca.core.executable_level_1.executable import Executable
from utca.core.executable_level_1.schema import (
    Input, Output, Transformable
)
from utca.core.predictor_level_2.predictor import Predictor
from utca.core.task_level_3.schema import NEROutputType

class Task(
    Executable[Input, Output]
):
    """
    Base task
    """
    def __init__(
        self,
        *,
        predictor: Predictor[Any, Any],
        preprocess: Optional[Component]=None,
        postprocess: Optional[Component]=None,
        input_class: Type[Input],
        output_class: Type[Output],
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            predictor (Predictor[Any, Any]): Predictor that will be used in task.

            preprocess (Optional[Component]): Component executed 
                before predictor.
            
            postprocess (Optional[Component]): Component executed
                after predictor.
            
            input_class (Type[Input]): Class for input validation.

            output_class (Type[Output]): Class for output validation.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(
            input_class=input_class, 
            output_class=output_class, 
            name=name,
        )
        self.predictor = predictor
        self._preprocess = preprocess
        self._postprocess = postprocess

    
    def process(
        self, 
        state: Transformable, 
        component: Optional[Component],
        evaluator: Evaluator
    ) -> Transformable:
        """
        Execute Component

        Args:
            state (Transformable): Current data.

            component (Optional[Component]): Component.
            
            evaluator (Evaluator): Evaluator in context of which executed.

        Returns:
            Transformable: Result of execution.
        """
        return component(state, evaluator) if component else state


    def invoke(
        self, input_data: Input, evaluator: Evaluator
    ) -> Dict[str, Any]:
        """
        Task main logic

        Args:
            input_data (Input): Validated input data.

            evaluator (Evaluator): Evaluator in context of which executed.

        Returns:
            Dict[str, Any]: Result of execution.
        """
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
    """
    Base NER task
    """
    ...