from typing import Dict, Any, Literal, Optional, Tuple, cast

from PIL import Image, ImageOps

from utca.core.executable_level_1.actions import Action

class ImageRead(Action[Dict[str, Any], Image.Image]):
    """
    Read image
    """
    def __init__(
        self,
        name: Optional[str]=None,
        default_key: str="image",
    ) -> None:
        """
        Args:
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.

            default_key (str, optional): What key will be used by default. 
                Defaults to "image".
        """
        super().__init__(name=name, default_key=default_key)


    def execute(self, input_data: Dict[str, Any]) -> Image.Image:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "path_to_file" (str): Path to image file;

        Raises:
            Exception: If unable to read image.

        Returns:
            Image.Image: Image.
        """
        try:
            return Image.open(input_data["path_to_file"]) # type: ignore
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
                "image" (Image.Image): Image;

                "path_to_file" (str): Path to image file;

        Raises:
            Exception: If unable to write image.
        """
        try:
            cast(Image.Image, input_data["image"]).save(input_data["path_to_file"]) # type: ignore
        except Exception as e:
            raise Exception(f"Unable to write image: {e}")


class ImageConvertChannels(Action[Image.Image, Image.Image]):
    """
    Convert image channels
    """
    def __init__(
        self, 
        channels_mode: Literal["RGB", "RGBA", "L", "P", "PA", "CMYK"]="RGB",
        name: Optional[str]=None,
        default_key: str="image",
    ):
        """
        Args:
            channels_mode (Literal["RGB", "RGBA", "L", "P", "PA", "CMYK"], optional): Channels mode to use.
                Defaults to "RGB".

            name (Optional[str], optional): Name for identification.
                    If equals to None, class name will be used. Defaults to None.

            default_key (str, optional): What key will be used by default. 
                Defaults to "image".
        """
        self.channels_mode = channels_mode
        super().__init__(name=name, default_key=default_key)


    def execute(self, input_data: Image.Image) -> Image.Image:
        """
        Args:
            input_data (Image.Image): Image.

        Returns:
            Image.Image: Coverted image.
        """
        return input_data.convert(self.channels_mode)


class ImageRotate(Action[Image.Image, Image.Image]):
    """
    Rotate image
    """
    def __init__(
        self, 
        angle: float, 
        resample: Image.Resampling=Image.Resampling.NEAREST,
        expand: bool=False,
        center: Optional[Tuple[float, float]]=None,
        translate: Optional[Tuple[float, float]]=None,
        fillcolor: Optional[Any]=None,
        name: Optional[str]=None,
        default_key: str="image",
    ) -> None:
        """
        Args:
            angle (float): Rotation angle in degrees counter clockwise.

            resample (Image.Resampling, optional): An optional resampling filter. This can be
                one of Resampling.NEAREST (use nearest neighbour), Resampling.BILINEAR (linear 
                interpolation in a 2x2 environment), or Resampling.BICUBIC (cubic spline 
                interpolation in a 4x4 environment). If the image has
                mode "1" or "P", it is set to Resampling.NEAREST. Defaults to Resampling.NEAREST.

            expand (bool, optional): Optional expansion flag. If true, expands the output
                image to make it large enough to hold the entire rotated image. If false,
                make the output image the same size as the input image. Defaults to False.
                
                Note that the expand flag assumes rotation around the center and no translation.

            center (Optional[Tuple[float, float]], optional): Optional center of rotation (a 2-tuple). 
                Origin is the upper left corner. Default is the center of the image.
                
            translate (Optional[Tuple[float, float]], optional): An optional post-rotate 
                translation (a 2-tuple).

            fillcolor (Optional[Any], optional): An optional color for area outside the rotated image.
                
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.

            default_key (str, optional): What key will be used by default. 
                Defaults to "image".
        """
        super().__init__(name=name, default_key=default_key)
        self.angle = angle
        self.resample = resample
        self.expand = expand
        self.center = center
        self.translate = translate
        self.fillcolor=fillcolor


    def execute(self, input_data: Image.Image) -> Image.Image:
        """
        Args:
            input_data (Image.Image): Image.

        Returns:
            Image.Image: Rotated image.
        """
        return input_data.rotate( # type: ignore
                angle=self.angle,
                resample=self.resample,
                expand=self.expand,
                center=self.center,
                translate=self.translate,
                fillcolor=self.fillcolor,
            )
    

class ImageResize(Action[Image.Image, Image.Image]):
    """
    Resize image
    """
    def __init__(
        self, 
        width: int, 
        height: int,
        resample: Optional[Image.Resampling]=None,
        box: Optional[Tuple[float, float, float, float]]=None,
        reducing_gap: Optional[float]=None,
        name: Optional[str]=None,
        default_key: str="image",
    ) -> None:
        """
        Args:
            width (int): New width in pixels.
            
            height (int): New height in pixels.

            resample (Optional[Image.Resampling], optional): An optional resampling filter.
                This can be one of Resampling.NEAREST, Resampling.BOX,
                Resampling.BILINEAR, Resampling.HAMMING, Resampling.BICUBIC or Resampling.LANCZOS.
                If the image has mode "1" or "P", it is always set to Resampling.NEAREST. 
                If the image mode specifies a number of bits, such as "I;16", then the default filter is
                Resampling.NEAREST. Otherwise, the default filter is Resampling.BICUBIC.
                Defaults to None

            box (Optional[Tuple[float, float, float, float]], optional): An optional 4-tuple of floats providing
                the source image region to be scaled. The values must be within (0, 0, width, height) rectangle.
                If None, the entire source is used. Defaults to None.

            reducing_gap (Optional[float], optional): Apply optimization by resizing the image
                in two steps. First, reducing the image by integer times using ~PIL.Image.Image.reduce.
                Second, resizing using regular resampling. The last step changes size no less than by 
                reducing_gap times. reducing_gap may be None (no first step is performed) or should be
                greater than 1.0. The bigger reducing_gap, the closer the result to the fair resampling.
                The smaller reducing_gap, the faster resizing. With reducing_gap greater or equal to 3.0,
                the result is indistinguishable from fair resampling in most cases. 
                Defaults to None (no optimization).
            
            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
            
            default_key (str, optional): What key will be used by default. 
                Defaults to "image".
        """
        super().__init__(name=name, default_key=default_key)
        self.height = height
        self.width = width
        self.resample = resample
        self.box = box
        self.reducing_gap = reducing_gap


    def execute(self, input_data: Image.Image) -> Image.Image:
        """
        Args:
            input_data (Image.Image): Image.

        Returns:
            Image.Image: Resized image.
        """
        return input_data.resize( # type: ignore
            (self.width, self.height),
            resample=self.resample,
            box=self.box,
            reducing_gap=self.reducing_gap,
        )
    

class ImagePad(Action[Image.Image, Image.Image]):
    """
    Pad image
    """
    def __init__(
        self, 
        width: int, 
        height: int,
        method: Image.Resampling=Image.Resampling.BICUBIC,
        color: Optional[Any]=None,
        centering: Tuple[float, float]=(0.5, 0.5),
        name: Optional[str]=None,
        default_key: str="image",
    ) -> None:
        """
        Args:
            width (int): New width in pixels.
            
            height (int): New height in pixels.

            method (Image.Resampling, optional): Resampling method to use. 
                Default is Resampling.BICUBIC.

            color (Optional[Any], optional): The background color of the padded image.
                Defaults to None.

            centering (Tuple[float, float], optional): Control the position of the original image within the
                  padded version. (0.5, 0.5) will keep the image centered 
                  (0, 0) will keep the image aligned to the top left (1, 1)
                  will keep the image aligned to the bottom right.

            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.
            
            default_key (str, optional): What key will be used by default. 
                Defaults to "image".
        """
        super().__init__(name=name, default_key=default_key)
        self.height = height
        self.width = width
        self.method = method
        self.color = color
        self.centering = centering


    def execute(self, input_data: Image.Image) -> Image.Image:
        """
        Args:
            input_data (Image.Image): Image.

        Returns:
            Image.Image: Padded image.
        """
        return ImageOps.pad(
            input_data,
            (self.width, self.height),
            method=self.method,
            color=self.color,
            centering=self.centering,
        )


class ImageCrop(Action[Image.Image, Image.Image]):
    """
    Crop image
    """
    def __init__(
        self, 
        box: Tuple[int, int, int, int],
        name: Optional[str]=None,
        default_key: str="image",
    ) -> None:
        """
        Args:
            box (Tuple[int, int, int, int]): Bbox for crop. x0, y0, x1, y1, where 
                x0, y0 - left top corner, x1, y1 - right bottom corner (relative in pixels).

            name (Optional[str], optional): Name for identification.
                If equals to None, class name will be used. Defaults to None.

            default_key (str, optional): What key will be used by default. 
                Defaults to "image".
        """
        super().__init__(name=name, default_key=default_key)
        self.box = box


    def execute(self, input_data: Image.Image) -> Image.Image:
        """
        Args:
            input_data (Image.Image): Image.

        Returns:
            Image.Image: Croped image.
        """
        return input_data.crop(self.box)