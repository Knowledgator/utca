from typing import Dict, Any, Type, Optional, Union

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
    def __init__(self, *, image: PILImage.Image):
        self.image = image


    def __setattr__(self, name: str, value: Any) -> None: # disable pydantic
        self.__dict__[name] = value


    def model_dump(
        self, 
        *, 
        mode: str='python', 
        include: Optional[Union[
            set[int], set[str], dict[int, Any], dict[str, Any]
        ]]=None,
        exclude: Optional[Union[
            set[int], set[str], dict[int, Any], dict[str, Any]
        ]]=None,
        by_alias: bool=False, 
        exclude_unset: bool=False,
        exclude_defaults: bool=False,
        exclude_none: bool=False, 
        round_trip: bool=False,
        warnings: bool=True
    ) -> Dict[str, Any]:
        return {'image': self.image}


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
    def __init__(self, *, path_to_file: str, image: PILImage.Image):
        self.image = image
        self.path_to_file = path_to_file


    def __setattr__(self, name: str, value: Any) -> None: # disable pydantic
        self.__dict__[name] = value


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