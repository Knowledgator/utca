from typing import Dict, Any, Optional, Tuple, cast

from PIL import Image, ImageOps

from core.executable_level_1.actions import Action, OneToOne

@OneToOne
class ImageRead(Action):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data['image'] = Image.open(input_data['path_to_file'])
        return input_data


@OneToOne
class ImageWrite(Action):
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data['image'].save(input_data['path_to_file'])
        return input_data


@OneToOne
class ImageRotate(Action):
    def __init__(self, rotation: float) -> None:
        self.rotation = rotation


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data['image'] = cast(
            Image.Image, input_data['image']
        ).rotate(self.rotation)
        return input_data
    

@OneToOne
class ImageResize(Action):
    def __init__(self, width: int, height: int) -> None:
        self.height = height
        self.width = width


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data['image'] = cast(
            Image.Image, input_data['image']
        ).resize((self.width, self.height))
        return input_data
    

@OneToOne
class ImagePad(Action):
    def __init__(self, width: int, height: int, color: Optional[str]=None) -> None:
        self.height = height
        self.width = width
        self.color = color


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data['image'] = ImageOps.pad(
            cast(Image.Image, input_data['image']),
            (self.width, self.height),
            color=self.color
        )
        return input_data
    

@OneToOne
class ImageCrop(Action):
    def __init__(self, box: Tuple[int, int, int, int]) -> None:
        self.box = box


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_data['image'] = cast(
            Image.Image, input_data['image']
        ).crop(self.box)
        return input_data