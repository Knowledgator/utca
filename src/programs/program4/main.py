from typing import Dict, Any, cast

from transformers import ( # type: ignore
    AutoFeatureExtractor, 
    AutoModelForImageClassification,
    AutoConfig
)

from core.model_level_2.transformers_image_classification import (
    TransformersImageClassificationConfig,
    TransformersImageClassification
)
from core.executable_level_1.schema import ExecuteFunction, PadImage
from core.datasource_level_2.image import (
    ImageReadInput,
    Image
)
from core.executable_level_1.interpreter import Evaluator

model_name = "facebook/deit-base-distilled-patch16-384"

labels = AutoConfig.from_pretrained(model_name).id2label # type: ignore

# Define model stage
model_stage = TransformersImageClassification( # type: ignore
    TransformersImageClassificationConfig(
        model=AutoModelForImageClassification.from_pretrained(model_name), # type: ignore
        feature_extractor=AutoFeatureExtractor.from_pretrained(model_name) # type: ignore
    )
)

def interpret_results(model_ouput: Dict[str, Any]) -> Dict[str, Any]:
    predicted_class_idx = model_ouput["outputs"]["logits"].argmax().item()
    return {"label": labels[predicted_class_idx]}


pipeline = (
    Image().read()
    | PadImage(width=224, height=224)
    | model_stage
    | ExecuteFunction(interpret_results)
)

# Image of German Shepherd Dog
image_input = ImageReadInput(path_to_file="programs/program4/test.jpg")

result = cast(Dict[str, Any], Evaluator(pipeline).run_program(image_input))
print(result)