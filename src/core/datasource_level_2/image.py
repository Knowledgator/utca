from typing import Dict, Any, Type, Optional

from PIL import Image as PILImage

from core.datasource_level_2.datasource import DatasourceManager, DatasourceAction
from core.datasource_level_2.schema import (
    DatasourceConfig,
    DatasourceInput,
    DatasourceOutput
)

class ImageReadInput(DatasourceInput):
    path_to_file: str


class ImageReadOutput(DatasourceOutput):
    image: PILImage.Image


class ImageRead(DatasourceAction[
    DatasourceConfig,
    ImageReadInput,
    ImageReadOutput
]):
    input_class: Type[ImageReadInput] = ImageReadInput
    output_class: Type[ImageReadOutput] = ImageReadOutput

    def invoke(self, input_data: ImageReadInput) -> Dict[str, Any]:
        return {'image': PILImage.open(input_data.path_to_file)}


    def invoke_batch(self, input_data: list[ImageReadInput]) -> list[Dict[str, Any]]:
        return [self.invoke(i) for i in input_data]


class ImageWriteInput(DatasourceInput):
    path_to_file: str
    image: PILImage.Image


class ImageWriteOutput(DatasourceOutput):
    ...


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


class Image(DatasourceManager[
    DatasourceConfig,
    ImageReadInput,
    ImageReadOutput,

    DatasourceConfig,
    ImageWriteInput,
    ImageWriteOutput,
]):
    def read(
        self, cfg: Optional[DatasourceConfig]=None,
    ) -> ImageRead:
        return ImageRead(cfg)

    
    def write(
        self, cfg: Optional[DatasourceConfig]=None,
    ) -> ImageWrite:
        return ImageWrite(cfg)