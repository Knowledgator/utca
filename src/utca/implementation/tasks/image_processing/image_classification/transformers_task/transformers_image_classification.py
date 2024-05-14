from typing import Any, Dict, List, Tuple, Type, Optional 

from pydantic import ConfigDict
from PIL import Image
from transformers import ( # type: ignore
    AutoImageProcessor,
    AutoModelForImageClassification,
)

from utca.core.executable_level_1.schema import (
    Input, Output, IOModel
)
from utca.core.executable_level_1.executor import ActionType
from utca.core.predictor_level_2.predictor import Predictor
from utca.core.task_level_3.task import Task
from utca.implementation.predictors.transformers_predictor.transformers_model import (
    TransformersModel,
    TransformersModelConfig
)
from utca.implementation.predictors.transformers_predictor.schema import (
    TransformersImageClassificationModelInput,
    TransformersLogitsOutput,
)
from utca.implementation.tasks.image_processing.image_classification.transformers_task.actions import (
    ImageClassificationPreprocessor,
    ImageClassificationSingleLabelPostprocessor,
)
from utca.implementation.datasources.image.actions import ImagePad

class TransformersImageClassificationInput(IOModel):
    """
    Args:
        image (Image.Image): Image to process.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    image: Image.Image


class TransformersImageClassificationOutput(IOModel):
    """
    Args:
        label (Optional[Tuple[str, float]]): Classified label and score.
    """
    label: Optional[Tuple[str, float]]


class TransformersImageClassificationMultilabelOutput(IOModel):
    """
    Args:
        labels (Dict[str, float]): Classified labels and scores.
    """
    labels: Dict[str, float]


class TransformersImageClassification(
    Task[Input, Output]
):
    """
    Basic image classification task
    """
    default_model = "facebook/deit-base-distilled-patch16-384"
    
    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[List[ActionType]]=None,
        postprocess: Optional[List[ActionType]]=None,
        input_class: Type[Input]=TransformersImageClassificationInput,
        output_class: Type[Output]=TransformersImageClassificationOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            predictor (Optional[Predictor[Any, Any]], optional): Predictor that will be used in task.
                If equals to None, default predictor will be used. Defaults to None.
            
            preprocess (Optional[List[ActionType]], optional): Chain of actions executed 
                before predictor. If equals to None, default chain will be used. Defaults to None.

                Default chain: 
                    [ImagePad, ImageClassificationPreprocessor]

                If default chain is used, ImageClassificationPreprocessor will use AutoImageProcessor
                from "facebook/deit-base-distilled-patch16-384" model.
            
            postprocess (Optional[List[ActionType]], optional): Chain of actions executed
                after predictor. If equals to None, default chain will be used. Defaults to None.

                Default chain: 
                [ImageClassificationSingleLabelPostprocessor]

                If default chain is used, ImageClassificationSingleLabelPostprocessor will use labels 
                from "facebook/deit-base-distilled-patch16-384" model.
            
            input_class (Type[Input], optional): Class for input validation. 
                Defaults to TransformersImageClassificationInput.
            
            output_class (Type[Output], optional): Class for output validation. 
                Defaults to TransformersImageClassificationOutput.
            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        if not predictor:
            model = AutoModelForImageClassification.from_pretrained(self.default_model) # type: ignore
            predictor=TransformersModel(
                TransformersModelConfig(
                    model=model # type: ignore
                ),
                input_class=TransformersImageClassificationModelInput,
                output_class=TransformersLogitsOutput,
            )
        
        if not preprocess:
            processor = AutoImageProcessor.from_pretrained(predictor.config._name_or_path) # type: ignore
            preprocess = [
                ImagePad(width=224, height=224).use(get_key="image"),
                ImageClassificationPreprocessor(
                    processor=processor # type: ignore
                )
            ]

        if not postprocess:
            labels = predictor.config.id2label # type: ignore
            postprocess = [
                ImageClassificationSingleLabelPostprocessor(
                    labels=labels # type: ignore
                )
            ]

        super().__init__(
            predictor=predictor,
            preprocess=preprocess,
            postprocess=postprocess,
            input_class=input_class, 
            output_class=output_class,
            name=name,
        )