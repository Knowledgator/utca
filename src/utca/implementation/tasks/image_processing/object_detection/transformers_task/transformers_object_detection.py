from typing import Any, List, Tuple, Type, Optional 

from pydantic import ConfigDict
from PIL import Image
from transformers import ( # type: ignore
    DetrImageProcessor,
    DetrForObjectDetection,
)

from utca.core.executable_level_1.component import Component
from utca.core.executable_level_1.schema import (
    Input, Output, IOModel
)
from utca.core.predictor_level_2.predictor import Predictor
from utca.core.task_level_3.task import Task
from utca.implementation.predictors.transformers_predictor.transformers_model import (
    TransformersModel,
    TransformersModelConfig
)
from utca.implementation.predictors.transformers_predictor.schema import (
    TransformersImageClassificationModelInput,
    TransformersDETROutput,
)
from utca.implementation.tasks.image_processing.object_detection.transformers_task.actions import (
    ObjectDetectionPreprocessor,
    DETRPostprocessor,
)

class TransformersObjectDetectionInput(IOModel):
    """
    Args:
        image (Image.Image): Image to process.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    image: Image.Image


class TransformersObjectDetectionOutput(IOModel):
    """
    Args:
        scores (List[float]): Probability scores.
        labels (List[str]): Classified labels.
        boxes (List[Tuple[float, float, float, float]]): Bounding boxes.
    """
    scores: List[float]
    labels: List[str]
    boxes: List[Tuple[float, float, float, float]]


class TransformersObjectDetection(
    Task[Input, Output]
):
    """
    Basic object detection task
    """
    default_model = "facebook/detr-resnet-50"
    
    def __init__(
        self,
        *,
        predictor: Optional[Predictor[Any, Any]]=None,
        preprocess: Optional[Component]=None,
        postprocess: Optional[Component]=None,
        input_class: Type[Input]=TransformersObjectDetectionInput,
        output_class: Type[Output]=TransformersObjectDetectionOutput,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            predictor (Optional[Predictor[Any, Any]], optional): Predictor that will be used in task.
                If equals to None, default predictor will be used. Defaults to None.
            
            preprocess (Optional[Component], optional): Component executed 
                before predictor. If equals to None, default component will be used. Defaults to None.

                Default component: 
                    ObjectDetectionPreprocessor

                If default component is used, ObjectDetectionPreprocessor will use DetrImageProcessor
                from "facebook/detr-resnet-50" model.
            
            postprocess (Optional[Component], optional): Component executed
                after predictor. If equals to None, default component will be used. Defaults to None.

                Default component: 
                    DETRPostprocessor

                If default component is used, DETRPostprocessor will use DetrImageProcessor and labels
                from "facebook/detr-resnet-50" model.
            
            input_class (Type[Input], optional): Class for input validation. 
                Defaults to TransformersObjectDetectionInput.
            
            output_class (Type[Output], optional): Class for output validation. 
                Defaults to TransformersObjectDetectionOutput.
            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.
        """
        if not predictor:
            model = DetrForObjectDetection.from_pretrained( # type: ignore
                self.default_model, revision="no_timm"
            )
            predictor=TransformersModel(
                TransformersModelConfig(
                    model=model # type: ignore
                ),
                input_class=TransformersImageClassificationModelInput,
                output_class=TransformersDETROutput,
            )
        
        if not preprocess or not postprocess:
            processor = DetrImageProcessor.from_pretrained( # type: ignore
                predictor.config._name_or_path, revision="no_timm"
            ) 

            if not preprocess:
                preprocess = ObjectDetectionPreprocessor(
                    processor=processor # type: ignore
                )

            if not postprocess:
                postprocess = DETRPostprocessor(
                    labels=predictor.config.id2label, # type: ignore
                    processor=processor # type: ignore
                )

        super().__init__(
            predictor=predictor,
            preprocess=preprocess,
            postprocess=postprocess,
            input_class=input_class, 
            output_class=output_class,
            name=name,
        )