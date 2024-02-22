from typing import Any, Optional, Union, Dict

from PIL import Image

from core.datasource_level_2.schema import (
    DatasourceInput,
    DatasourceOutput
)

class ImageReadInput(DatasourceInput):
    path_to_file: str


class ImageReadOutput(DatasourceOutput):
    def __init__(self, *, image: Image.Image):
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
    

class ImageWriteInput(DatasourceInput):
    def __init__(self, *, path_to_file: str, image: Image.Image):
        self.image = image
        self.path_to_file = path_to_file


    def __setattr__(self, name: str, value: Any) -> None: # disable pydantic
        self.__dict__[name] = value


class ImageWriteOutput(DatasourceOutput):
    ...