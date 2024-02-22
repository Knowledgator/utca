from typing import Type, Dict, Any

from PIL import Image

from core.datasource_level_2.datasource import DatasourceAction
from core.datasource_level_2.schema import DatasourceConfig
from implementation.datasources.image.schema import (
    ImageReadInput,
    ImageReadOutput,
    ImageWriteInput,
    ImageWriteOutput
)

class ImageRead(DatasourceAction[
    DatasourceConfig,
    ImageReadInput,
    ImageReadOutput
]):
    input_class: Type[ImageReadInput] = ImageReadInput
    output_class: Type[ImageReadOutput] = ImageReadOutput

    def invoke(self, input_data: ImageReadInput) -> Dict[str, Any]:
        return {'image': Image.open(input_data.path_to_file)}


    def invoke_batch(self, input_data: list[ImageReadInput]) -> list[Dict[str, Any]]:
        return [self.invoke(i) for i in input_data]


class ImageWrite(DatasourceAction[
    DatasourceConfig,
    ImageWriteInput,
    ImageWriteOutput
]):
    input_class: Type[ImageWriteInput] = ImageWriteInput 
    output_class: Type[ImageWriteOutput] = ImageWriteOutput

    def invoke(self, input_data: ImageWriteInput) -> Dict[str, Any]:
        input_data.image.save(input_data.path_to_file)
        return {}


    def invoke_batch(self, input_data: list[ImageWriteInput]) -> list[Dict[str, Any]]:
        for i in input_data:
            self.invoke(i)
        return []