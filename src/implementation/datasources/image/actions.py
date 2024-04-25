from typing import Dict, Any, Optional, Tuple, cast

from PIL import Image, ImageOps

from core.executable_level_1.actions import Action

class ImageRead(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Read image
    """
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'path_to_file' (str): Path to image file;

        Raises:
            Exception: If unable to read image.

        Returns:
            Dict[str, Any]: Expected keys:
                'image' (PIL.Image.Image): Image;
        """
        try:
            return {"image": Image.open(input_data["path_to_file"])}
        except Exception as e:
            raise Exception(f"Unable to read image: {e}")
        

class ImageWrite(Action[Dict[str, Any], None]):
    """
    Write image
    """
    def execute(self, input_data: Dict[str, Any]) -> None:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'image' (PIL.Image.Image): Image;

                'path_to_file' (str): Path to image file;

        Raises:
            Exception: If unable to write image.
        """
        try:
            input_data['image'].save(input_data['path_to_file'])
        except Exception as e:
            raise Exception(f"Unable to write image: {e}")


class ImageRotate(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Rotate image
    """
    def __init__(
        self, rotation: float, name: Optional[str]=None,
    ) -> None:
        """
        Args:
            rotation (float): Rotation angle in degrees.

            name (Optional[str], optional): name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.rotation = rotation


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'image' (PIL.Image.Image): Image;

        Raises:
            Exception: If unable to read image.

        Returns:
            Dict[str, Any]: Expected keys:
                'image' (PIL.Image.Image): Rotated image;
        """
        return {
            "image": cast(
                Image.Image, input_data["image"]
            ).rotate(self.rotation)
        }
    

class ImageResize(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Resize image
    """
    def __init__(
        self, width: int, height: int, name: Optional[str]=None,
    ) -> None:
        """
        Args:
            width (int): New width in pixels.
            
            height (int): New height in pixels.
            
            name (Optional[str], optional): name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.height = height
        self.width = width


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'image' (PIL.Image.Image): Image;

        Raises:
            Exception: If unable to read image.

        Returns:
            Dict[str, Any]: Expected keys:
                'image' (PIL.Image.Image): Resized image;
        """
        return {
            "image": cast(
                Image.Image, input_data["image"]
            ).resize((self.width, self.height))
        }
    

class ImagePad(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Pad image
    """
    def __init__(
        self, 
        width: int, 
        height: int, 
        color: Optional[str]=None,
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            width (int): New width in pixels.
            
            height (int): New height in pixels.

            color (Optional[str], optional): The background color of the padded image.
                Defaults to None.

            name (Optional[str], optional): name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.height = height
        self.width = width
        self.color = color


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'image' (PIL.Image.Image): Image;

        Raises:
            Exception: If unable to read image.

        Returns:
            Dict[str, Any]: Expected keys:
                'image' (PIL.Image.Image): Padded image;
        """
        return {
            "image": ImageOps.pad(
                cast(Image.Image, input_data['image']),
                (self.width, self.height),
                color=self.color
            )
        }    


class ImageCrop(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Crop image
    """
    def __init__(
        self, 
        box: Tuple[int, int, int, int],
        name: Optional[str]=None,
    ) -> None:
        """
        Args:
            box (Tuple[int, int, int, int]): Bbox for crop. x0, y0, x1, y1, where 
                x0, y0 - left top corner, x1, y1 - right bottom corner (relative in pixels).

            name (Optional[str], optional): name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
        """
        super().__init__(name)
        self.box = box


    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                'image' (PIL.Image.Image): Image;

        Raises:
            Exception: If unable to read image.

        Returns:
            Dict[str, Any]: Expected keys:
                'image' (PIL.Image.Image): Croped image;
        """
        return {
            "image": cast(
                Image.Image, input_data["image"]
            ).crop(self.box)
        }