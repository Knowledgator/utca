from typing import Any, Dict, Type, Optional
from gliner import GLiNER # type: ignore

from utca.core.executable_level_1.schema import Output
from utca.core.predictor_level_2.predictor import Predictor
from utca.core.executable_level_1.interpreter import Evaluator

from utca.implementation.predictors.gliner_predictor.schema import (
    GLiNERPredictorConfig, 
    GLiNERPredictorInput, 
    GLiNERPredictorOutput
)   
from utca.implementation.predictors.utils import ensure_dict

class GLiNERPredictor(
    Predictor[GLiNERPredictorInput, Output]
):
    """
    GLiNER predictor. This predictor is specifically build to use GLiNER approach - https://github.com/urchade/GLiNER. 
    """
    def __init__(
        self, 
        cfg: Optional[GLiNERPredictorConfig]=None,
        input_class: Type[GLiNERPredictorInput]=GLiNERPredictorInput,
        output_class: Type[Output]=GLiNERPredictorOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            cfg (GLiNERPredictorConfig, optional): Configuration for predictor.
                If value equals to None, default GLiNERPredictorConfig configuration
                will be used. Defaults to None.
            
            input_class (Type[Input], optional): Class for input validation.
                Defaults to GLiNERPredictorInput.
            
            output_class (Type[Output], optional): Class for output validation.
                Defaults to GLiNERPredictorOutput.
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        if cfg is None:
            cfg = GLiNERPredictorConfig()
        self.model = GLiNER.from_pretrained(cfg.model_name).to(cfg.device) # type: ignore
        super().__init__(
            input_class=input_class,
            output_class=output_class,
            name=name,
        )


    def invoke(self, input_data: GLiNERPredictorInput, evaluator: Evaluator) -> Dict[str, Any]:
        """
        Call pipeline

        Args:
            input_data (Input): Validated input.

            evaluator (Evaluator): Evaluator in context of wich executed.

        Returns:
            Dict[str, Any]: Result of execution.
        """
        if not input_data.labels:
            return {"output": [[]]*len(input_data.texts)}
        labels = set(input_data.labels)
        texts = input_data.texts
        outputs = self.model.batch_predict_entities(texts=texts, labels=labels) # type: ignore
        return ensure_dict(outputs)


    @property
    def config(self) -> Any:
        """
        Model configuration
        """
        return self.model.config # type: ignore