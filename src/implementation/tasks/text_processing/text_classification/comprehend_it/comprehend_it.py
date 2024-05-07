from typing import Any, List, Optional, Type

from core.executable_level_1.schema import Input, Output
from core.executable_level_1.executor import ActionType
from core.predictor_level_2.predictor import Predictor
from core.task_level_3.task import Task
from implementation.predictors.comprehend_it.predictor import (
    ComprehendItPredictor, 
    ComprehendItPredictorInput, 
    ComprehendItPredictorOutput
)

class ComprehendIt(
    Task[Input, Output]
):
    """
    Task for text classification
    """
    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[List[ActionType]]=None,
        postprocess: Optional[List[ActionType]]=None,
        input_class: Type[Input]=ComprehendItPredictorInput,
        output_class: Type[Output]=ComprehendItPredictorOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            predictor (Predictor[Any, Any]): Predictor that will be used in task. 
                If equals to None, default ComprehendItPredictor will be used. Defaults to None.

            preprocess (Optional[List[Action[Any, Any]]]): Chain of actions executed 
                before predictor. Defaults to None.
            
            postprocess (Optional[List[Action[Any, Any]]]): Chain of actions executed
                after predictor. Defaults to None.
            
            input_class (Type[Input]): Class for input validation. Defaults to ComprehendItPredictorInput.

            output_class (Type[Output]): Class for output validation. Defaults to ComprehendItPredictorOutput.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        if not predictor:
            predictor = ComprehendItPredictor()

        super().__init__(
            predictor=predictor,
            preprocess=preprocess or [],
            postprocess=postprocess or [],
            input_class=input_class, 
            output_class=output_class,
            name=name,
        )

