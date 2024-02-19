from typing import Dict, Any, cast
import json

from transformers import ( # type: ignore
    AutoFeatureExtractor, 
    AutoModelForImageClassification
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

# Define model stage
model_stage = TransformersImageClassification( # type: ignore
    TransformersImageClassificationConfig(
        model=AutoModelForImageClassification.from_pretrained(model_name), # type: ignore
        feature_extractor=AutoFeatureExtractor.from_pretrained(model_name) # type: ignore
    )
)

def interpret_results(model_ouput: Dict[str, Any]) -> Dict[str, Any]:
    with open('test_labels.json', 'r') as f:
        labels = json.load(f)
    predicted_class_idx = model_ouput['outputs'].logits.argmax().item()
    return {'label': labels[predicted_class_idx]}


pipeline = (
    Image().read()
    | PadImage(width=224, height=224)
    | model_stage
    | ExecuteFunction(interpret_results)
)

# Image of German Shepherd Dog
input = ImageReadInput(path_to_file='test.jpg')

result = cast(Dict[str, Any], Evaluator(pipeline).run(input))
print(result)